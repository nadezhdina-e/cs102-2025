from collections import deque
from copy import deepcopy
from random import choice, randint
from typing import Deque, List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord1: Tuple[int, int], coord2: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord1:
    :param coord2:
    :return:
    """
    x1, y1 = coord1
    x2, y2 = coord2
    wall_x, wall_y = (x1 + x2) // 2, (y1 + y2) // 2
    grid[wall_x][wall_y] = " "
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

    for x, y in empty_cells:
        directions = []
        if x - 2 >= 0:
            directions.append((x - 2, y))
        if y + 2 < cols:
            directions.append((x, y + 2))
        if directions:
            next_cell = choice(directions)
            grid = remove_wall(grid, (x, y), next_cell)

    print(
        f"Выберите способ выбора точек входа в лабиринт и выхода из него:\n1 - По умолчанию\n2 - Рандомным путем"
        f"\n3 - Введите свои значения "
    )
    exit_choice = str(input("Выведите число 1/2/3 "))
    if exit_choice == "1":
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1
    elif exit_choice == "2":
        if random_exit:
            x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
            y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
            y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
        else:
            x_in, y_in = 0, cols - 2
            x_out, y_out = rows - 1, 1
    else:
        print(
            f"Введите точку входа. Она может располагаться только на сторонах лабиринта, поэтому одна из координат "
            f"должна равняться 14 или 0. Введите 2 числа через пробел "
        )
        dots = input().split(" ")
        x_in, y_in = int(dots[0]), int(dots[1])
        print(f"Введите точку выхода. Условия аналогичны ")
        dots = input().split(" ")
        x_out, y_out = int(dots[0]), int(dots[1])
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


def make_step(grid: List[List[Union[str, int]]], x_neigh, y_neigh, k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :param y_neigh:
    :param x_neigh:
    :return:
    """
    rows, cols = len(grid), len(grid[0])
    if 0 <= x_neigh < rows and 0 <= y_neigh < cols:
        if grid[x_neigh][y_neigh] == " " or grid[x_neigh][y_neigh] == 0:
            grid[x_neigh][y_neigh] = k
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], start: Tuple[int, int], end: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param start:
    :param end:
    :return:
    """
    if grid[end[0]][end[1]] == 0:
        return None

    rows, cols = len(grid), len(grid[0])
    grid_copy = deepcopy(grid)

    queue: Deque[Tuple[int, int, int]] = deque()
    queue.append((start[0], start[1], 1))
    visited = set()
    visited.add(start)
    grid_copy[start[0]][start[1]] = 1

    while queue:
        x, y, dist = queue.popleft()
        if (x, y) == end:
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid_copy[nx][ny] in (" ", "X") and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    grid_copy[nx][ny] = dist + 1
                    queue.append((nx, ny, dist + 1))
    path = []
    x, y = end
    dist = grid_copy[x][y]  # type: ignore
    path.append((x, y))

    while dist > 1:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid_copy[nx][ny] == dist - 1:
                    path.append((nx, ny))
                    x, y = nx, ny
                    dist -= 1
                    break

    path.reverse()
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    if (x == 0 and y == 0) or (x == 0 and y == 14) or (x == 14 and y == 0) or (x == 14 and y == 14):
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
                    maze = make_step(maze, i - 1, j, k)
                    maze = make_step(maze, i + 1, j, k)
                    maze = make_step(maze, i, j - 1, k)
                    maze = make_step(maze, i, j + 1, k)
        if not found_cell:
            return maze, None
    path = shortest_path(maze, start, end)
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
