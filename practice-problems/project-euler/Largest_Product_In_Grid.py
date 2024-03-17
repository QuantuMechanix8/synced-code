import time
def get_max_product(array, num_sequential = 0):
    if num_sequential == 0:
        num_sequential = len(array)
    max = 0
    currentProduct = 1
    if num_sequential>len(array):
        num_sequential = len(array)
    for index in range(len(array) - (num_sequential - 1)):
        for value in range(num_sequential):
            currentProduct *= int(array[index + value])
        if currentProduct > max:
            max = currentProduct
        currentProduct = 1
    return max

def test_get_max_product():
    assert get_max_product([1,2,3,4,5], 2) == 20
    assert get_max_product([1,2,3,4,5], 3) == 60
    assert get_max_product([4]) == 4
    assert get_max_product([1,2,3,4,5], 1) == 5
    assert get_max_product([1,2,3,4,5], 5) == 120


def get_1D_array_from_2D(grid, startIndex = (0,0), direction = "E"):
    direction = direction.upper()
    # converts compass direction to vector direction
    if direction == "N":
        direction = (-1,0)
    elif direction == "NE":
        direction = (-1,1)
    elif direction == "E":
        direction = (0,1)
    elif direction == "SE":
        direction = (1,1)
    elif direction == "S":
        direction = (1,0)
    elif direction == "SW":
        direction = (1,-1)
    elif direction == "W":
        direction = (0,-1)
    elif direction == "NW":
        direction = (-1,-1)
    else:
        raise ValueError("direction must be one of the following: {'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'}")
    
    finished = False
    created_array = []
    currentPos = startIndex
    current_Pos_X = currentPos[1]
    current_Pos_Y = currentPos[0]
    while not finished:
        if current_Pos_X<0 or current_Pos_X>len(grid[0])-1 or current_Pos_Y<0 or current_Pos_Y>len(grid)-1:
            finished = True
            break
        created_array.append(grid[current_Pos_Y][current_Pos_X])
        current_Pos_X, current_Pos_Y = current_Pos_X + direction[1], current_Pos_Y + direction[0]
    return created_array

def test_get_1D_array_from_2D():
    grid = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
    assert get_1D_array_from_2D(grid) == [1,2,3,4,5]
    assert get_1D_array_from_2D(grid, (4,0), "N") == [21,16,11,6,1]
    assert get_1D_array_from_2D(grid, (1,1), "SE") == [7,13,19,25]
        
def get_all_lines_in_rectangular_grid(grid, min_elements = 1):
    if min_elements > len(grid[0]):
        min_elements = len(grid[0])
    elif min_elements <1:
        min_elements = 1
    lines = []
    
    # horizontal lines
    """finds lines rightward of leftmost column"""
    for side_index in range(len(grid)):
        line = get_1D_array_from_2D(grid, (side_index, 0), "E")
        if len(line) >= min_elements:
            lines.append(line)
            
    # vertical lines
    """finds lines downward from top row"""
    for top_index in range(len(grid[0])):
        line = get_1D_array_from_2D(grid, (0, top_index), "S")
        if len(line) >= min_elements:
            lines.append(line)
            
    # diagonal lines
    
    # SE lines
    """finds lines SE from leftmost column"""
    for side_index in range(len(grid)):
        line = get_1D_array_from_2D(grid, (side_index, 0), "SE")
        if len(line) >= min_elements:
            lines.append(line)
    """finds lines SE from top row column"""
    for top_index in range(len(grid[0])):
        line = get_1D_array_from_2D(grid, (0, top_index), "SE")
        if len(line) >= min_elements:
            lines.append(line)
    # NE lines
    """finds lines NE from leftmost column"""
    for side_index in range(len(grid)):
        line = get_1D_array_from_2D(grid, (side_index, 0), "NE")
        if len(line) >= min_elements:
            lines.append(line)
    """finds lien NE from bottom row"""
    for bottom_index in range(len(grid[0])):
        line = get_1D_array_from_2D(grid, (len(grid)-1, bottom_index), "NE")
        if len(line) >= min_elements:
            lines.append(line)
    
    for line in lines:
        if len(line) < min_elements:
            lines.remove(line)
    return lines
    

def get_max_product_in_grid(grid, num_sequential):
    lines = get_all_lines_in_rectangular_grid(grid)
    max = 0
    for line in lines:
        line_product = get_max_product(line, num_sequential)
        if line_product>max:
            max = line_product
    return max

grid = []
with open(r"/home/saulivor/Desktop/Work/Coding/Python/OtherPrograms/Project Euler/grid.txt", "r") as f:
    for line in f.readlines():
        grid_row = line.split()
        grid_row = [int(x) for x in grid_row]
        grid.append(grid_row)
start = time.time()
get_max_product_in_grid(grid, 4)
end = time.time()
print(end-start)

