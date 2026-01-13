import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        result = []
        for i in range(self.rows):
            if randomize:
                line = [random.randint(0, 1) for _ in range(self.cols)]
            else:
                line = [0 for _ in range(self.cols)]
            result.append(line)

        return result

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []

        for dff_r in [-1, 0, 1]:
            for dff_c in [-1, 0, 1]:
                if dff_r == 0 and dff_c == 0:
                    continue
                neigbour_row = row + dff_r
                neigbour_col = col + dff_c

                if 0 <= neigbour_row < self.rows and 0 <= neigbour_col < self.cols:
                    neighbours.append(self.curr_generation[neigbour_row][neigbour_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        rows_count = self.rows
        cols_count = self.cols
        new_grid = [[0 for _ in range(cols_count)] for _ in range(rows_count)]

        for row in range(rows_count):
            for col in range(cols_count):
                neighbours = self.get_neighbours((row, col))
                live_neighbours = sum(neighbours)
                current_cell = self.curr_generation[row][col]

                if current_cell == 1:
                    if live_neighbours == 2 or live_neighbours == 3:
                        new_grid[row][col] = 1
                    else:
                        new_grid[row][col] = 0
                else:
                    if live_neighbours == 3:
                        new_grid[row][col] = 1
                    else:
                        new_grid[row][col] = 0

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return True

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            lines = f.readlines()
        rows_count = len(lines)
        cols_count = len(lines[0].strip()) if lines else 0
        game = GameOfLife((rows_count, cols_count), randomize=False, max_generations=float("inf"))
        grid = []
        for line in lines:
            row = [int(char) for char in line.strip()]
            grid.append(row)
        game.curr_generation = grid
        game.prev_generation = [[0] * cols_count for _ in range(rows_count)]

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                line = "".join(str(cell) for cell in row)
