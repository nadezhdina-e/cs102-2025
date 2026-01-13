import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        height = self.life.rows
        width = self.life.cols
        max_y, max_x = screen.getmaxyx()
        if height + 3 >= max_y or width + 3 >= max_x:
            return

        screen.addch(0, 0, "<")
        screen.addch(0, width + 1, ">")
        screen.addch(height + 1, 0, "<")
        screen.addch(height + 1, width + 1, ">")

        for position in range(1, width + 1):
            screen.addch(0, position, "=")
            screen.addch(height + 1, position, "=")

        for line in range(1, height + 1):
            screen.addch(line, 0, "!")
            screen.addch(line, width + 1, "!")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        field = self.life.curr_generation

        for row_num in range(self.life.rows):
            for col_num in range(self.life.cols):

                if field[row_num][col_num] == 1:
                    screen.addch(row_num + 1, col_num + 1, "#")
                else:
                    screen.addch(row_num + 1, col_num + 1, ".")

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)

        try:
            running = True
            while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                info = f" Поколение: {self.life.generations} (Q для выхода) "
                screen.addstr(self.life.rows + 2, 0, info)
                screen.refresh()
                self.life.step()
                curses.napms(100)
                screen.nodelay(True)
                key = screen.getch()
                if key == ord("q") or key == ord("Q"):
                    running = False

        finally:
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()
