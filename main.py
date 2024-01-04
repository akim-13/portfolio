import numpy as np
import time

class ContradictionException(Exception):
    pass

# (1, 1) (1, 2) (1, 3)   (1, 4) (1, 5) (1, 6)   (1, 7) (1, 8) (1, 9)
# (2, 1) (2, 2) (2, 3)   (2, 4) (2, 5) (2, 6)   (2, 7) (2, 8) (2, 9)
# (3, 1) (3, 2) (3, 3)   (3, 4) (3, 5) (3, 6)   (3, 7) (3, 8) (3, 9)
#
# (4, 1) (4, 2) (4, 3)   (4, 4) (4, 5) (4, 6)   (4, 7) (4, 8) (4, 9)
# (5, 1) (5, 2) (5, 3)   (5, 4) (5, 5) (5, 6)   (5, 7) (5, 8) (5, 9)
# (6, 1) (6, 2) (6, 3)   (6, 4) (6, 5) (6, 6)   (6, 7) (6, 8) (6, 9)
#
# (7, 1) (7, 2) (7, 3)   (7, 4) (7, 5) (7, 6)   (7, 7) (7, 8) (7, 9)
# (8, 1) (8, 2) (8, 3)   (8, 4) (8, 5) (8, 6)   (8, 7) (8, 8) (8, 9)
# (9, 1) (9, 2) (9, 3)   (9, 4) (9, 5) (9, 6)   (9, 7) (9, 8) (9, 9)

# `cells = [(1, 1), (1, 2), ..., (9, 8), (9, 9)]`.
cells = [ (row, column) for row in range(1, 10) for column in range(1, 10) ]
units = { cell: [] for cell in cells }
peers = {}

# Populate `units`.
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
for row in range(1, 10, 3):
    for col in range(1, 10, 3):
        box_unit = [ (row+dx, col+dy) for dx in range(3) for dy in range(3) ]
        for cell in box_unit:
            units[cell].append(box_unit)

# Populate `peers`.
for cell in cells:
    units_of_a_cell = units[cell]
    # Flatten and exclude the current cell.
    flattened_units_of_a_cell = [ cell_iter for unit in units_of_a_cell for cell_iter in unit if cell_iter != cell ]
    # Convert into a set to enforce uniqueness and allow for O(1) lookups.
    peers[cell] = set(flattened_units_of_a_cell)


def remove_digit_from_peers(digit, cell, grid):
    for peer in peers[cell]:
        # TODO: Figure out if this ever happens what to do with it.
        # If there are no available digits for given a cell.
        if not grid[peer]:
            raise ContradictionException
        grid[peer] = grid[peer].replace(digit, '')
    return grid


def assign_and_propagate(digit, cell, grid):
    # When the cell is empty (`digit == 0`) it has to keep the default `available_digits` value.
    if digit != '0':
        grid[cell] = digit

    if len(digit) > 1:
        grid[cell] = digit
        return grid
    
    cell_has_one_possible_value = len(grid[cell]) == 1
    if cell_has_one_possible_value:
        grid = remove_digit_from_peers(digit, cell, grid)

    digits_counter = { digit: {'count': 0, 'cell': None} for digit in '123456789' }
    # Insert a digit if a unit has one possible place for a value.
    for unit in units[cell]:
        potential_naked_twins = {}
        potential_naked_twins_counter = {}

        for cell_iter in unit:
            for digit_iter in grid[cell_iter]:
                digits_counter[digit_iter]['count'] += 1
                digits_counter[digit_iter]['cell'] = cell_iter

            cell_has_two_possible_values = len(grid[cell_iter]) == 2
            if cell_has_two_possible_values:
                potential_naked_twins[cell_iter] = grid[cell_iter]

        for cell, digits in potential_naked_twins.items():
            potential_naked_twins_counter.setdefault(digits, []).append(cell)

        # Filter `potential_naked_twins_counter` to include only those digit pairs that occur exactly twice.
        naked_twins = { digits: cells for digits, cells in potential_naked_twins_counter.items() if len(cells) == 2 }
        if naked_twins:
            for digits, cells in naked_twins.items():
                first_twin   = cells[0]
                second_twin  = cells[1]
                first_digit  = digits[0]
                second_digit = digits[1]
                for cell in unit:
                    # TODO: May be redundant.
                    if not grid[cell]:
                        raise ContradictionException
                    if (cell != first_twin) and (cell != second_twin):
                        grid[cell] = grid[cell].replace(first_digit, '')
                        grid[cell] = grid[cell].replace(second_digit, '')

        for digit_key, value in digits_counter.items():
            unit_missing_possible_digit = value['count'] == 0
            if unit_missing_possible_digit: 
                raise ContradictionException

            cell_has_multiple_possible_values = len(grid[value['cell']]) > 1
            unit_has_one_possible_place_for_value = (value['count'] == 1) and (cell_has_multiple_possible_values)
            if unit_has_one_possible_place_for_value:
                assign_and_propagate(digit_key, value['cell'], grid)

            # Reset the values for the iteration over the next unit.
            digits_counter[digit_key]['count'] = 0
            digits_counter[digit_key]['cell'] = None

                

def generate_solution(numpy_arrays):
    flattened_numpy_array = [ str(item_cell) for array in numpy_arrays for item_cell in array ]
    available_digits = '123456789'
    # Initialize an empty greed (i.e. every cell can take any digit).
    grid = { cell: available_digits for cell in cells }

    for cell, digit in zip(cells, flattened_numpy_array):
        assign_and_propagate(digit, cell, grid)

    return grid


def convert_grid_to_np_array(grid):
    np_grid = np.empty((9, 9), dtype=object)

    for (row, col), available_digits in grid.items():
        try:
            available_digits = int(available_digits)
        except:
            available_digits = '●'
        np_grid[row-1, col-1] = available_digits
    return np_grid


def display_sudoku(grid):
    horizontal_line = ' ' + '+'.join(['-'*7]*3)
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print(horizontal_line)
        try:
            row_str = '| ' + ' | '.join(' '.join(str(int(cell)) for cell in row[j:j+3]) for j in range(0, 9, 3)) + ' |'
        except:
            row_str = '| ' + ' | '.join(' '.join(str(cell) for cell in row[j:j+3]) for j in range(0, 9, 3)) + ' |'
        print(row_str)
    print()


def main():
    difficulty = 'medium'
    sudokus = np.load(f'data/{difficulty}_puzzle.npy')
    sudokus_solutions = np.load(f'data/{difficulty}_solution.npy')

    # Convert solutions to int if necessary.
    sudokus_solutions = sudokus_solutions.astype(int)

    solving_times = []

    print('Generating solutions...')
    output = False
    for j in range(25):
        for i in range(0, 15):
            if output:
                print('Sudoku:')
                display_sudoku(sudokus[i])

            start_time = time.time()

            try:
                solution = generate_solution(sudokus[i])
                solution = convert_grid_to_np_array(solution)
            except ContradictionException:
                solution = np.full((9, 9), -1)

            end_time = time.time()
            solving_time = end_time - start_time
            solving_times.append(solving_time)

            if output:
                print(f'Solving time: {solving_time} seconds')
                print('Generated solution:')
                display_sudoku(solution)
                print('Actual solution:')
                display_sudoku(sudokus_solutions[i])
                print('---------------------------------------------------------------------------------')

            if not np.array_equal(solution, sudokus_solutions[i]):
                raise ContradictionException


    average_time = round(sum(solving_times) / len(solving_times), 4)
    max_time = round(max(solving_times), 4)
    print(f'Average solving time: {average_time} seconds')
    print(f'Maximum solving time: {max_time} seconds')


if __name__ == "__main__":
    main()
