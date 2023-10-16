import math

#TODO create function to check available rows, columns and subsquares for each number and then narrows this info down to give a single place

"""initialises user inputted sudoku grid as 2d array"""
def initialise_grid():
    # grid size has to be a square number - so should validate this
    valid_grid_size = False
    while not valid_grid_size:
        try:
            grid_size = int(
                input("What is the size of the grid i.e. (4) -> 4x4, (9) -> 9x9: ")
            )
            int(
                math.sqrt(grid_size)
            )  # will raise exception if grid_size isn't square num
            valid_grid_size = True
        except:
            print("Invalid grid_size, try again\n")
            continue

    sudoku_grid = [[0] * grid_size] * grid_size

    for i in range(0, grid_size):
        grid_line_str = input(
            f"Please enter the (comma separated) elements in row {i}: "
        )
        grid_line = list(map(int, grid_line_str.split(",")))
        sudoku_grid[i] = grid_line
    return sudoku_grid


"""Solves sudoku grid"""
def solve(sudoku_grid):
    pass


def next_move(sudoku_grid):
    grid_size = len(sudoku_grid[0])
    digits = list(range(grid_size))
    for digit in digits:
        pass


def get_columns(sudoku_grid):
    grid_size = len(sudoku_grid[0])
    return [[sudoku_grid[i][j] for i in range(grid_size)] for j in range(grid_size)]


def get_rows(sudoku_grid):
    grid_size = len(sudoku_grid[0])
    return [[sudoku_grid[i][j] for j in range(grid_size)] for i in range(grid_size)]


def get_subsquares(sudoku_grid):
    grid_size = len(sudoku_grid[0])

    # side length of each subsquare but also the number of subsquares in each row/column
    subsquares_in_row = int(math.sqrt(grid_size))

    return [
        get_subsquare(sudoku_grid, i * subsquares_in_row, j * subsquares_in_row)
        for i in range(subsquares_in_row)
        for j in range(subsquares_in_row)
    ]


"""Return an array of the subsquare within grid 'starting' (top-left) at i,j"""
def get_subsquare(sudoku_grid, initial_row, initial_column):
    subsquare_side_length = int(math.sqrt(len(sudoku_grid[0])))
    subsquare = []

    for i in range(subsquare_side_length):
        for j in range(subsquare_side_length):
            row = initial_row + i
            column = initial_column + j
            subsquare.append(sudoku_grid[row][column])

    return subsquare


"""Return an array of bools to delineate whether the number can be put in that subarray

i.e. possible_places([[0,1], [0, 0], [2,1], [2,0]], 1) => [F, T, F, T]"""
def possible_subarrays(subarrays, i):
    return [any(item==i for item in subarray) for subarray in subarrays]


"""Prints nicely formatted matrix with equal spacing"""
def print_matrix(matrix):
    flattened_matrix = [
        matrix[i][j] for i in range(len(matrix[0])) for j in range(len(matrix))
    ]
    longest_item = max(map(lambda x: len(str(x)), flattened_matrix))

    # print each item formatted to all be the length of the longest item, separated by spaces
    print("[")
    for row in matrix:
        for item in row:
            print(f"{item:{longest_item}}", end=" ")
        print()
    print("]\n")


# sudoku_grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
sudoku_grid = [[4 * j + i for i in range(4)] for j in range(4)]
print_matrix(sudoku_grid)
# print(f"sudoku grid is:\n{sudoku_grid}")

print_matrix(get_subsquares(sudoku_grid))
# print(get_columns(sudoku_grid))
# print(get_rows(sudoku_grid))
