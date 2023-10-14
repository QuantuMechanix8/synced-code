import math

"""initialises user inputted sudoku grid as 2d array"""
def initialise_grid():
    # grid size has to be a square number - so should validate this
    grid_size = int(input("What is the size of the grid i.e. (4) -> 4x4, (9) -> 9x9: "))
    sudoku_grid = [[0]*grid_size]*grid_size

    for i in range(0,grid_size):
        grid_line_str = input(f"Please enter the (comma separated) elements in row {i}: ")
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


def get_squares(sudoku_grid):
    grid_size = len(sudoku_grid[0])
    square_size = int(math.sqrt(grid_size))



sudoku_grid = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]
print(f"sudoku grid is:\n{sudoku_grid}")
print(get_columns(sudoku_grid))
#print(get_rows(sudoku_grid))