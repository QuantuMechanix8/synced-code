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
    digits = list(range)