import numpy as np
import time
import random

# Frequently used constants, populated in `main()`.
cells = [ (row, column) for row in range(1, 10) for column in range(1, 10) ]
units = { cell: [] for cell in cells }
peers = { }

INVALID_SOLUTION = { cell: '-1' for cell in cells }
ALL_AVAILABLE_DIGITS = '123456789'

class ContradictionException(Exception):
    pass


def populate_units():
    # Populate the row and column units.
    for cell in cells:
        row_unit = []
        col_unit = []
        for cell_iter in cells:
            cell_on_the_same_row = cell_iter[0] == cell[0]
            if cell_on_the_same_row:
                row_unit.append(cell_iter)
            cell_in_the_same_column = cell_iter[1] == cell[1]
            if cell_in_the_same_column:
                col_unit.append(cell_iter)
        units[cell] += [row_unit, col_unit]

    # Populate the 3x3 box units.
    for row in range(1, 10, 3):
        for col in range(1, 10, 3):
            box_unit = [ (row+dx, col+dy) for dx in range(3) for dy in range(3) ]
            for cell in box_unit:
                units[cell].append(box_unit)


def populate_peers():
    for cell in cells:
        # Flatten and exclude the current cell.
        flattened_units_of_a_cell = [ cell_iter for unit in units[cell] for cell_iter in unit if cell_iter != cell ]
        # Convert into a set to enforce uniqueness and allow for O(1) lookups.
        peers[cell] = set(flattened_units_of_a_cell)


def display_sudoku(np_array):
    horizontal_separator = '|' + '+'.join(['-------']*3) + '|'
    for i, row in enumerate(np_array):
        if (i % 3 == 0) and (i != 0):
            print(horizontal_separator)
        row_str = '| ' + ' | '.join(' '.join(str(cell) for cell in row[j:j+3]) for j in range(0, 9, 3)) + ' |'
        print(row_str)
    print()


def convert_grid_to_np_array(grid):
    np_grid = np.empty((9, 9), dtype=object)

    for (row, col), available_digits in grid.items():
        try:
            available_digits = int(available_digits)
        except:
            available_digits = '●'
        np_grid[row-1, col-1] = available_digits

    return np_grid


def find_least_constraining_values(mrv_cell, grid):
    count_and_available_digit_pairs = []
    for digit in grid[mrv_cell]:
        occurrence_counter = 0
        for peer in peers[mrv_cell]:
            if digit in grid[peer]:
                occurrence_counter += 1
        count_and_available_digit_pairs.append((occurrence_counter, digit))
    least_constraining_values_sorted_pairs = sorted(count_and_available_digit_pairs, reverse=True)
    least_constraining_digits = [ pair[1] for pair in least_constraining_values_sorted_pairs ]

    return least_constraining_digits


def find_cell_with_min_remaining_values(grid):
    mrv_cell = None
    # Any cell has less 9 or less available values, hence choose 10 as "infinity".
    min_remaining_values = 10

    for cell in cells:
        num_of_remaining_values = len(grid[cell])
        if 1 < num_of_remaining_values < min_remaining_values:
            mrv_cell = cell
            if num_of_remaining_values == 2:
                break
            min_remaining_values = num_of_remaining_values

    return mrv_cell


def recursive_depth_first_search(grid):
    # Base case that may terminate recursion early.
    solution_is_found = all(len(grid[cell]) == 1 for cell in cells)
    if solution_is_found:
        return grid

    # Find values for MRV and LCV heuristics.
    mrv_cell = find_cell_with_min_remaining_values(grid)
    if mrv_cell is None:
        return INVALID_SOLUTION
    least_constraining_digits_sorted = find_least_constraining_values(mrv_cell, grid)

    for digit in least_constraining_digits_sorted:
        new_grid = grid.copy()
        try:
            new_grid = constrain_cell_to_single_digit(digit, mrv_cell, new_grid)
            solution = recursive_depth_first_search(new_grid)
            solution_is_valid = not np.array_equal(solution, INVALID_SOLUTION)
            if solution_is_valid:
                return solution
        except ContradictionException:
            pass

    return INVALID_SOLUTION


def fill_in_hidden_singles(digit, cell, grid):
    for unit in units[cell]:
        num_of_occurences_in_unit = 0
        last_occured_in_cell = None

        for cell_in_unit in unit:
            if digit in grid[cell_in_unit]:
                num_of_occurences_in_unit += 1
                last_occured_in_cell = cell_in_unit

        if last_occured_in_cell is not None:
            if num_of_occurences_in_unit == 1:
                grid = constrain_cell_to_single_digit(digit, last_occured_in_cell, grid)
        else:
            raise ContradictionException

    return grid


def eliminate_current_digit_from_peers(cell, grid):
    for peer in peers[cell]:
        grid = propagate_digit_elimination(grid[cell], peer, grid)

    return grid


def check_for_naked_twins(cell, grid):
    for unit in units[cell]:
        for potential_naked_twin in unit:

            naked_twins_found = (len(grid[potential_naked_twin]) == 2) and (grid[cell] in grid[potential_naked_twin]) and (potential_naked_twin != cell)

            if naked_twins_found:
                naked_twin = potential_naked_twin
                first_twin_digit = grid[naked_twin][0]
                second_twin_digit = grid[naked_twin][1]

                for cell_of_unit in unit:
                    if (cell_of_unit != naked_twin) and (cell_of_unit != cell):
                        grid = propagate_digit_elimination(first_twin_digit, cell_of_unit, grid)
                        grid = propagate_digit_elimination(second_twin_digit, cell_of_unit, grid)

        if naked_twins_found:
            break

    return grid


def propagate_digit_elimination(digit, cell, grid):
    digit_is_present = digit in grid[cell]

    if digit_is_present:
        grid[cell] = grid[cell].replace(digit, '')
    else:
        return grid

    num_of_remaining_digits = len(grid[cell])

    if num_of_remaining_digits == 2:
        grid = check_for_naked_twins(cell, grid)
    elif num_of_remaining_digits == 1:
        grid = eliminate_current_digit_from_peers(cell, grid)
    elif num_of_remaining_digits == 0:
        raise ContradictionException

    grid = fill_in_hidden_singles(digit, cell, grid)

    return grid


def constrain_cell_to_single_digit(digit, cell, grid):
    for digit_to_be_eliminated in grid[cell]:
        if digit_to_be_eliminated != digit:
            grid = propagate_digit_elimination(digit_to_be_eliminated, cell, grid)

    return grid


def initialize_grid_with_given_digits(given_digits):
    grid = { cell: ALL_AVAILABLE_DIGITS for cell in cells }

    for digit, cell in zip(given_digits, cells):
        cell_is_empty = digit == '0'

        if cell_is_empty:
            continue

        try:
            grid = constrain_cell_to_single_digit(digit, cell, grid)
        except ContradictionException:
            return INVALID_SOLUTION

    return grid
                

def sudoku_solver(numpy_array):
    flattened_numpy_array = [ str(item_cell) for array in numpy_array for item_cell in array ]
    grid = initialize_grid_with_given_digits(flattened_numpy_array)
    grid_solution = recursive_depth_first_search(grid)
    numpy_array_solution = convert_grid_to_np_array(grid_solution)

    return numpy_array_solution


def main():
    populate_units()
    populate_peers()

    difficulty = 'hard'
    sudokus = np.load(f'data/{difficulty}_puzzle.npy')
    sudokus_solutions = np.load(f'data/{difficulty}_solution.npy').astype(int)

    print('Generating solutions...', end='\n\n')

    solving_times = []
    output_enabled = True

    if output_enabled:
        test_n_times = 1
    else:
        test_n_times = 128

    for _ in range(test_n_times):
        for i in range(15):
            if output_enabled:
                print(f'Sudoku number {i+1} ({difficulty}):')
                display_sudoku(sudokus[i])

            start_time = time.time()

            # TODO: Terminate execution after 29.9 second.
            solution = sudoku_solver(sudokus[i])

            end_time = time.time()
            solving_time = end_time - start_time
            solving_times.append(solving_time)

            if output_enabled:
                print(f'Generated solution (generated in {round(solving_time, 4)} seconds):')
                display_sudoku(solution)
                print('Actual solution:')
                display_sudoku(sudokus_solutions[i])
                print('=================================================================')
                print()

            if not np.array_equal(solution, sudokus_solutions[i]):
                raise ContradictionException

    average_time = round(sum(solving_times) / len(solving_times), 4)
    max_time = round(max(solving_times), 4)
    print(f'Average solving time: {average_time} seconds')
    print(f'Maximum solving time: {max_time} seconds')


if __name__ == "__main__":
    main()

