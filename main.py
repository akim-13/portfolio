import numpy as np
import time
import copy

# Frequently used constants, populated in `main()`.
cells = [ (row, column) for row in range(1, 10) for column in range(1, 10) ]
units = { cell: [] for cell in cells }
peers = { }

# Global variable to track the elapsed time since the start of the solution generation.
# IMPORTANT: Ensure `start_time` is defined and used globally to prevent incorrect triggering of 
# the time-out condition in `recursive_depth_first_search`, which could lead to an erroneous 
# `INVALID_SOLUTION` return.
start_time = time.time()

INVALID_SOLUTION = { cell: '-1' for cell in cells }
ALL_AVAILABLE_DIGITS = '123456789'


class ContradictionException(Exception):
    """
    Custom exception used to indicate a contradiction encountered during Sudoku solving.

    This exception is raised when the Sudoku solver reaches a state where a valid solution is no longer possible
    under the current assumptions, necessitating backtracking or termination of the solving process.
    """
    pass


def populate_units():
    """
    Populate the row, column, and 3x3 box units for each cell in a Sudoku grid.

    A 'unit' of a cell is an element of the global `units` dict, where each key is a cell 
    and each value is a list of three lists: all cells on the same row as the key cell, 
    all cells in the same column, and all cells in the same standard 3x3 box of cells.
    """
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
    """
    Populate the peers for each cell in a Sudoku grid.

    A 'peer' of a cell is an element of the global `peers` dict, where each key is a cell
    and each value is a set of all cells that are in the same three units as the key cell.
    Importantly, the key cell itself is excluded from the set.
    """
    for cell in cells:
        # Flatten and exclude the current cell.
        flattened_units_of_a_cell = [ cell_iter for unit in units[cell] for cell_iter in unit if cell_iter != cell ]
        # Convert into a set to enforce uniqueness and allow for O(1) lookups.
        peers[cell] = set(flattened_units_of_a_cell)


def display_sudoku(np_array):
    """
    Display a Sudoku puzzle in a human-readable format.

    Args:
        `np_array` (numpy.ndarray): A 9x9 NumPy array representing the Sudoku puzzle.
    """
    horizontal_separator = '|' + '+'.join(['-------']*3) + '|'
    for i, row in enumerate(np_array):
        if (i % 3 == 0) and (i != 0):
            print(horizontal_separator)
        row_str = '| ' + ' | '.join(' '.join(str(cell) for cell in row[j:j+3]) for j in range(0, 9, 3)) + ' |'
        print(row_str)
    print()


def convert_grid_to_np_array(grid):
    """
    Convert a grid dictionary to a NumPy array representing a Sudoku puzzle.

    Args:
        `grid` (dict): A dictionary where keys are cell coordinates (tuples) and values are strings of available digits.

    Return:
        `np_grid` (numpy.ndarray): A 9x9 NumPy array representing the Sudoku puzzle.
    """
    np_grid = np.empty((9, 9), dtype=object)

    for (row, col), available_digits in grid.items():
        try:
            available_digits = int(available_digits)
        except:
            available_digits = '●'
        np_grid[row-1, col-1] = available_digits

    return np_grid


def find_least_constraining_values(mrv_cell, grid):
    """
    Identify the least constraining values for the given cell using the Least Constraining Value heuristic.

    Args:
        `mrv_cell` (tuple): The cell (row, column) with the Minimum Remaining Values.
        `grid` (dict): The Sudoku grid as a dictionary.

    Return:
        `least_constraining_digits_sorted` (list): A list of digits sorted by their constraining effect on peers.
    """
    count_and_available_digit_pairs = []
    for digit in grid[mrv_cell]:
        occurrence_counter = 0
        for peer in peers[mrv_cell]:
            if digit in grid[peer]:
                occurrence_counter += 1
        count_and_available_digit_pairs.append((occurrence_counter, digit))
    least_constraining_values_sorted_pairs = sorted(count_and_available_digit_pairs, reverse=True)
    least_constraining_digits_sorted = [ pair[1] for pair in least_constraining_values_sorted_pairs ]

    return least_constraining_digits_sorted


def find_cell_with_min_remaining_values(grid):
    """
    Find the cell with the Minimum Remaining Values (remaining available digits) in the Sudoku grid.

    Args:
        `grid` (dict): The Sudoku grid as a dictionary.

    Return:
        `mrv_cell` (tuple or None): The cell with minimum remaining values, or None if no such cell exists.
    """
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
    """
    Perform a recursive depth-first search to solve the Sudoku puzzle.

    Args:
        `grid` (dict): The Sudoku grid as a dictionary.

    Return:
        `grid` (dict): The solved grid, or INVALID_SOLUTION if no solution exists.
    """
    solution_is_found = all(len(grid[cell]) == 1 for cell in cells)
    elapsed_time = time.time() - start_time
    time_threshold_exceeded = elapsed_time >= 29.99

    # Base case that may terminate recursion early.
    if solution_is_found:
        return grid
    elif time_threshold_exceeded:
        return INVALID_SOLUTION

    # Define the Minimum Remaining Values and Least Constraining Values heuristics.
    mrv_cell = find_cell_with_min_remaining_values(grid)
    # This should never happen, however it is better to be safe than sorry.
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
            # If a contradiction is encountered, discard this branch and try the next digit.
            pass

    # If all possibilities are exhausted without finding a valid solution, return an invalid solution.
    return INVALID_SOLUTION


def fill_in_hidden_singles(digit, cell, grid):
    """
    Fill in hidden singles for the given digit and cell in the Sudoku grid.

    Args:
        `digit` (str): The digit to check for hidden singles.
        `cell` (tuple): The cell (row, column) in the grid.
        `grid` (dict): The Sudoku grid as a dictionary.

    Return:
        `grid` (dict): The updated grid after filling in hidden singles.
    """
    for unit in units[cell]:
        num_of_occurences_in_unit = 0
        last_occured_in_cell = None

        for cell_in_unit in unit:
            if digit in grid[cell_in_unit]:
                num_of_occurences_in_unit += 1
                last_occured_in_cell = cell_in_unit

        if (last_occured_in_cell) and (num_of_occurences_in_unit == 1):
            grid = constrain_cell_to_single_digit(digit, last_occured_in_cell, grid)
        elif not last_occured_in_cell:
            raise ContradictionException

    return grid


def eliminate_current_digit_from_peers(cell, grid):
    """
    Eliminate the current digit from the peers of the given cell.

    Args:
        `cell` (tuple): The cell (row, column) from which to eliminate the digit.
        `grid` (dict): The Sudoku grid as a dictionary.

    Return:
        `grid` (dict): The updated grid after elimination.
    """
    for peer in peers[cell]:
        grid = propagate_digit_elimination(grid[cell], peer, grid)

    return grid


def check_for_naked_twins(cell, grid):
    """
    Check for and process naked twins in the units of the specified cell.

    Args:
        `cell` (tuple): The cell (row, column) to check for naked twins.
        `grid` (dict): The Sudoku grid as a dictionary.

    Return:
        `grid` (dict): The updated grid after processing naked twins.
    """
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
    """
    Propagate the elimination of a digit (i.e. recursively) from a specified cell throughout the grid.

    Args:
        `digit` (str): The digit to eliminate.
        `cell` (tuple): The cell (row, column) from which to eliminate the digit.
        `grid` (dict): The Sudoku grid as a dictionary.

    Return:
        `grid` (dict): The updated grid after propagating digit elimination.
    """
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
    """
    Constrain a cell to a single digit and propagate this constraint through the grid.

    Args:
        `digit` (str): The digit to assign to the cell.
        `cell` (tuple): The cell (row, column) to constrain.
        `grid` (dict): The Sudoku grid as a dictionary.

    Return:
        `grid` (dict): The updated grid after constraining the cell.
    """
    for digit_to_be_eliminated in grid[cell]:
        if digit_to_be_eliminated != digit:
            grid = propagate_digit_elimination(digit_to_be_eliminated, cell, grid)

    return grid


def initialize_grid_with_given_digits(given_digits):
    """
    Initialize the Sudoku grid with the given digits.

    The `grid` is a dictionary with 81 keys as all possible cells, and strings 
    of digits that can be assigned to a cell as their corresponding values.

    Args:
        `given_digits` (list): A list of digits to initialize the grid with.

    Return:
        `grid` (dict): The initialized grid, or INVALID_SOLUTION if a contradiction occurs.
    """
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
    """
    Generate a solution to a Sudoku puzzle represented as a NumPy array.

    Args:
        `numpy_array` (numpy.ndarray): A 9x9 NumPy array representing a Sudoku puzzle, where 0 denotes an empty cell.

    Return:
        `numpy_array_solution` (numpy.ndarray): A 9x9 NumPy array representing the solved Sudoku puzzle, or an array filled with -1 if no solution is found.
    """
    flattened_numpy_array = [ str(item_cell) for array in numpy_array for item_cell in array ]
    grid = initialize_grid_with_given_digits(flattened_numpy_array)
    grid_solution = recursive_depth_first_search(grid)
    numpy_array_solution = convert_grid_to_np_array(grid_solution)

    return numpy_array_solution


def main():
    global start_time

    populate_units()
    populate_peers()

    difficulty = 'hard'
    sudokus = np.load(f'data/{difficulty}_puzzle.npy')
    sudokus_solutions = np.load(f'data/{difficulty}_solution.npy').astype(int)

    print('Generating solutions...')

    solving_times = []
    incorrect_solutions_counter = 0
    num_of_sudokus = len(sudokus)

    sudoku_output_enabled = False
    if sudoku_output_enabled:
        test_n_times = 1
    else:
        test_n_times = 128

    print(f'The test (difficulty "{difficulty}") will be run {test_n_times} time(s).', end='\n\n')

    for n in range(test_n_times):
        for i in range(num_of_sudokus):
            sudoku = copy.deepcopy(sudokus[i])
            if sudoku_output_enabled:
                print(f'Sudoku number {i+1}:')
                display_sudoku(sudoku)

            # IMPORTANT: It is mandatory to use `time.time()` when testing, failure to do
            # so may result in erroneous assignment of `INVALID_SOLUTION` to `solution`.
            start_time = time.time()

            solution = sudoku_solver(sudoku)

            end_time = time.time()
            solving_time = end_time - start_time
            solving_times.append(solving_time)

            if sudoku_output_enabled:
                print(f'Generated solution (generated in {round(solving_time, 4)} seconds):')
                display_sudoku(solution)
                print('Actual solution:')
                display_sudoku(sudokus_solutions[i])

            if not np.array_equal(solution, sudokus_solutions[i]):
                print('ERROR: The generated solution does not match the actual one.')
                incorrect_solutions_counter += 1

            if sudoku_output_enabled:
                print('='*64, end='\n\n')

        num_of_correct_solutions = num_of_sudokus - incorrect_solutions_counter
        print(f'Test {n+1}/{test_n_times} completed.')
        print(f'{num_of_correct_solutions}/{num_of_sudokus} solutions are correct.', end='\n\n')

    average_time = round(sum(solving_times) / len(solving_times), 4)
    max_time = round(max(solving_times), 4)
    print(f'Average solving time: {average_time} seconds')
    print(f'Maximum solving time: {max_time} seconds')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nKEYBOARD INTERRUPT INITIATED.')
    except Exception as e:
        print(f'ERROR:\n{e}')
