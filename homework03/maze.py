from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    x, y = coord
    direction = choice(("up", "right"))
    if direction == "right":
        if y + 2 < len(grid[0]) and grid[x][y + 1] == "■":
            grid[x][y + 1] = " "
        elif x - 1 > 0 and grid[x - 1][y] == "■":
            grid[x - 1][y] = " "
    elif direction == "up":
        if x - 1 > 0 and grid[x - 1][y] == "■":
            grid[x - 1][y] = " "
        elif y + 2 < len(grid[0]) and grid[x][y + 1] == "■":
            grid[x][y + 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = False) -> List[List[Union[str, int]]]:
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
        y_out = y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1
    if x_in == 0:
        grid[x_in][y_in] = " "
        if x_in + 1 < rows:
            grid[x_in + 1][y_in] = " "
    elif x_in == rows - 1:
        grid[x_in][y_in] = " "
        if x_in - 1 >= 0:
            grid[x_in - 1][y_in] = " "
    elif y_in == 0:
        grid[x_in][y_in] = " "
        if y_in + 1 < cols:
            grid[x_in][y_in + 1] = " "
    elif y_in == cols - 1:
        grid[x_in][y_in] = " "
        if y_in - 1 >= 0:
            grid[x_in][y_in - 1] = " "

    if x_out == 0:
        grid[x_out][y_out] = " "
        if x_out + 1 < rows:
            grid[x_out + 1][y_out] = " "
    elif x_out == rows - 1:
        grid[x_out][y_out] = " "
        if x_out - 1 >= 0:
            grid[x_out - 1][y_out] = " "
    elif y_out == 0:
        grid[x_out][y_out] = " "
        if y_out + 1 < cols:
            grid[x_out][y_out + 1] = " "
    elif y_out == cols - 1:
        grid[x_out][y_out] = " "
        if y_out - 1 >= 0:
            grid[x_out][y_out - 1] = " "

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
    new_grid = deepcopy(grid)
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if new_grid[nx][ny] == 0:
                            new_grid[nx][ny] = k + 1
    return new_grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Находит кратчайший путь от exit_coord к клетке со значением 1.
    """
    if not grid:
        return None
    x, y = exit_coord
    rows, cols = len(grid), len(grid[0])
    current_value = grid[x][y]  # type: ignore
    if not isinstance(current_value, (int, float)):
        return None
    path = [(x, y)]
    while current_value > 1:  # type: ignore
        found = False
        for dff_x, dff_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbour_x, neighbour_y = x + dff_x, y + dff_y
            if 0 <= neighbour_x < rows and 0 <= neighbour_y < cols:
                cell = grid[neighbour_x][neighbour_y]
                if isinstance(cell, int) and cell == current_value - 1:
                    path.append((neighbour_x, neighbour_y))
                    x, y = neighbour_x, neighbour_y
                    current_value = cell
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
        walls = 0
        if x == 0 and y == 0:
            if x + 1 < rows and grid[x + 1][y] == "■":
                walls += 1
            if y + 1 < cols and grid[x][y + 1] == "■":
                walls += 1
        elif x == 0 and y == cols - 1:
            if x + 1 < rows and grid[x + 1][y] == "■":
                walls += 1
            if y - 1 >= 0 and grid[x][y - 1] == "■":
                walls += 1
        elif x == rows - 1 and y == 0:
            if x - 1 >= 0 and grid[x - 1][y] == "■":
                walls += 1
            if y + 1 < cols and grid[x][y + 1] == "■":
                walls += 1
        elif x == rows - 1 and y == cols - 1:
            if x - 1 >= 0 and grid[x - 1][y] == "■":
                walls += 1
            if y - 1 >= 0 and grid[x][y - 1] == "■":
                walls += 1
        if walls == 2:
            return True

    elif x == 0 or y == 0 or x == rows - 1 or y == cols - 1:
        walls = 0
        for dff_x, dff_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbour_x, neighbour_y = x + dff_x, y + dff_y
            if not (0 <= neighbour_x < rows and 0 <= neighbour_y < cols):
                walls += 1
            elif grid[neighbour_x][neighbour_y] == "■":
                walls += 1
        if walls == 4:
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
        if encircled_exit(maze, start):
            return maze, None
        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                if maze[i][j] == " " or maze[i][j] == "X":
                    maze[i][j] = 0
        maze[start[0]][start[1]] = 1
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

    # for i in range(len(result)):
    #     for j in range(len(result[0])):
    #         if isinstance(result[i][j], int):
    #             if (i, j) in path_set:
    #                 if (i, j) in original_exits:
    #                     result[i][j] = "X"
    #                 else:
    #                     result[i][j] = "X"
    #             else:
    #                 result[i][j] = " "

    # return result


if __name__ == "__main__":
    # GRID = bin_tree_maze(15, 15)
    # print(pd.DataFrame(GRID))
    # _, PATH = solve_maze(GRID)
    # MAZE = add_path_to_grid(GRID, PATH)
    # print(pd.DataFrame(MAZE))
    GRID = bin_tree_maze(15, 15)
    print("Maze:")
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    if PATH:
        MAZE = add_path_to_grid(GRID, PATH)
        print("\nSolution:")
        print(pd.DataFrame(MAZE))
    else:
        print("No path found!")
