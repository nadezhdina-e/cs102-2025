import random
import typing as tp
import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.grid_matrix = None
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.grid_matrix = self.create_grid(randomize = True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)

            self.draw_grid()
            self.draw_lines()
            self.grid_matrix = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        self.grid_matrix = []
        for i in range(self.cell_height):
            row = []
            for j in range(self.cell_width):
                if randomize is True:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = 0
                row.append(cell_value)
            self.grid_matrix.append(row)
        return self.grid_matrix


    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell_rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                if self.grid_matrix[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("green"), cell_rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"), cell_rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                new_row = row + i
                new_col = col + j
                if 0 <= new_row < self.cell_height and 0 <= new_col < self.cell_width:
                    neighbours.append(self.grid_matrix[new_row][new_col])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid(randomize=False)

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                current_cell = self.grid_matrix[i][j]
                neighbours = self.get_neighbours((i, j))
                live_neighbours = sum(neighbours)
                if current_cell == 1:  # Клетка жива
                    if live_neighbours < 2 or live_neighbours > 3:
                        new_grid[i][j] = 0  # Умирает
                    else:
                        new_grid[i][j] = 1  # Выживает
                else:  # Клетка мертва
                    if live_neighbours == 3:
                        new_grid[i][j] = 1  # Оживает
                    else:
                        new_grid[i][j] = 0  # Остается мертвой

        return new_grid


if __name__ == "__main__":
    from pprint import pprint as pp
    game = GameOfLife(320, 240, 40)
    print("Randomized grid (6x8):")
    random.seed(42)
    grid = game.create_grid(randomize=True)
    pp(grid)
    print("\nStarting graphical interface...")
    game = GameOfLife(640, 480, 10, 1)  # Другие параметры для GUI
    game.run()