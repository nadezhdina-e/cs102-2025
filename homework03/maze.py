from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    row, col = coord
    last_col_index = len(grid[0]) - 1
    selected_direction = choice(["up", "right"])
    if selected_direction == "up":
        can_go_up = row > 1
        if can_go_up:
            grid[row - 1][col] = " "
        else:
            can_go_right = col < last_col_index - 1
            if can_go_right:
                grid[row][col + 1] = " "
    else:  # direction == "right"
        can_go_right = col < last_col_index - 1
        if can_go_right:
            grid[row][col + 1] = " "
        else:
            can_go_up = row > 1
            if can_go_up:
                grid[row - 1][col] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:

                if i > 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if i < rows - 1 and grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if j > 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
                if j < cols - 1 and grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1
    return grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Находит кратчайший путь от exit_coord к клетке со значением 1.
    """
    if not grid:
        return None
    x, y = exit_coord
    rows, cols = len(grid), len(grid[0])
    current_value = grid[x][y]  # type: ignore
    if isinstance(current_value, str):
        try:
            current_value = int(current_value)
        except ValueError:
            return None
    if current_value == 1:
        return [exit_coord]
    path = [(x, y)]
    while current_value > 1:  # type: ignore
        found = False
        for dff_x, dff_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbour_x, neighbour_y = x + dff_x, y + dff_y
            if 0 <= neighbour_x < rows and 0 <= neighbour_y < cols:
                cell = grid[neighbour_x][neighbour_y]
                if isinstance(cell, str):
                    try:
                        cell = int(cell)
                    except ValueError:
                        continue
                if cell == current_value - 1:
                    path.append((neighbour_x, neighbour_y))
                    x, y = neighbour_x, neighbour_y
                    current_value -= 1
                    found = True
                    break
        if not found:
            return None
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    y, x = coord

    corner_positions = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]
    if (y, x) in corner_positions:
        return True

    if y == 0:
        if grid[y + 1][x] != " ":
            return True
    elif x == cols - 1:
        if grid[y][x - 1] != " ":
            return True
    elif y == rows - 1:
        if grid[y - 1][x] != " ":
            return True
    elif x == 0:
        if grid[y][x + 1] != " ":
            return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    maze = deepcopy(grid)
    exits = get_exits(maze)
    if len(exits) != 2:
        return maze, None
    else:
        start, end = exits[1], exits[0]
        for possible_exit in exits:
            if encircled_exit(grid, possible_exit):
                return grid, None
        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                if maze[i][j] == " ":
                    maze[i][j] = 0
        maze[start[0]][start[1]] = 1
        maze[end[0]][end[1]] = 0
        k = 1
        max_steps = len(maze) * len(maze[0])
        while maze[end[0]][end[1]] == 0 and k <= max_steps:
            maze = make_step(maze, k)
            k += 1
        if maze[end[0]][end[1]] == 0:
            return maze, None
        path_back = shortest_path(maze, end)
        if not path_back:
            return maze, None
        res = path_back[::-1]
        return maze, res


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if not path:
        return grid
    result = deepcopy(grid)
    path_list: List[Tuple[int, int]]
    if isinstance(path, tuple):
        path_list = [path]
    else:
        path_list = path

    for coord in path_list:
        x, y = coord
        result[x][y] = "X"

    return result


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
