from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    x, y = coord
    last_col = len(grid[0]) - 1
    direction = choice(("up", "right"))
    if direction == "up":
        if x > 1:
            grid[x - 1][y] = " "
        elif y < last_col - 1:
            grid[x][y + 1] = " "
    else:
        if y < last_col - 1:
            grid[x][y + 1] = " "
        elif x > 1:
            grid[x - 1][y] = " "
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
        remove_wall(grid, cell)

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
    rows, cols = len(grid), len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows, cols = len(grid), len(grid[0])
    next_k = k + 1
    new_grid = deepcopy(grid)
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] != k:
                continue
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and new_grid[nx][ny] == 0:
                    new_grid[nx][ny] = next_k
    return grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Находит кратчайший путь от exit_coord к клетке со значением 1.
    """
    x, y = exit_coord
    if grid[x][y] == 0:
        return None
    rows, cols = len(grid), len(grid[0])
    current_value = grid[x][y]  # type: ignore
    path = [(x, y)]
    while current_value > 1:  # type: ignore
        found = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == current_value - 1:  # type: ignore
                    path.append((nx, ny))
                    x, y = nx, ny
                    current_value -= 1  # type: ignore
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
    x, y = coord
    rows, cols = len(grid), len(grid[0])
    if (
        (x == 0 and y == 0)
        or (x == 0 and y == cols - 1)
        or (x == rows - 1 and y == 0)
        or (x == rows - 1 and y == cols - 1)
    ):
        return True
    if x == 0 and grid[x + 1][y] != " ":
        return True
    if x == 14 and grid[x - 1][y] != " ":
        return True
    if y == 0 and grid[x][y + 1] != " ":
        return True
    if y == 14 and grid[x][y - 1] != " ":
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

    start, end = exits[0], exits[1]
    maze[start[0]][start[1]] = 1
    maze[end[0]][end[1]] = 0

    k = 1
    while maze[end[0]][end[1]] == 0:
        k += 1
        found_cell = False
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == k - 1:
                    found_cell = True
                    maze = make_step(maze, k)
                    maze = make_step(maze, k)
                    maze = make_step(maze, k)
                    maze = make_step(maze, k)
        if not found_cell:
            return maze, None
    path = shortest_path(maze, end)
    if not path:
        return maze, None
    path_length = len(path) - 1
    expected_length = int(maze[end[0]][end[1]]) - 1
    if path_length != expected_length:
        for x, y in path[1:-1]:
            maze[x][y] = " "
        return solve_maze(maze)
    return maze, path


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
    path_set = set(path)
    original_exits = get_exits(grid)

    for i in range(len(result)):
        for j in range(len(result[0])):
            if isinstance(result[i][j], int):
                if (i, j) in path_set:
                    if (i, j) in original_exits:
                        result[i][j] = "X"
                    else:
                        result[i][j] = "X"
                else:
                    result[i][j] = " "

    return result


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    MAZE, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(MAZE, PATH)
    print(pd.DataFrame(MAZE))
