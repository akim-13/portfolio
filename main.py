import numpy as np

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
peers = dict()

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
        # TODO: Figure out if it's a valid case and what to do with it.
        # If there are no available digits for given a cell.
        if not grid[peer]:
            return None
        grid[peer] = grid[peer].replace(digit, '')
    return grid


def generate_solution(numpy_arrays):
    flattened_numpy_array = [ str(item_cell) for array in numpy_arrays for item_cell in array ]
    available_digits = '123456789'
    # Initialize an empty greed (i.e. every cell can take any digit).
    grid = { cell: available_digits for cell in cells }

    print(grid)
    first_assignment = True
    for cell, digit in zip(cells, flattened_numpy_array):
        # When the cell is empty (`digit == 0`) it has to keep the default `available_digits` value.
        if digit != '0':
            grid[cell] = digit
        
        cell_has_one_possible_value = len(grid[cell]) == 1
        if cell_has_one_possible_value:
            remove_digit_from_peers(digit, cell, grid)

        # TODO: Insert a digit if a unit has one possible place for a value.

    print()
    print(grid)


    return grid

def main():
    easy_sudokus = np.load("data/very_easy_puzzle.npy")
    easy_sudokus_solutions = np.load("data/very_easy_solution.npy")
    print(easy_sudokus[0])
    generate_solution(easy_sudokus[0])
    print(easy_sudokus_solutions[0])

if __name__ == "__main__":
    main()
