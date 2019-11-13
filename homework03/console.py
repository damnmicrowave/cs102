import curses

from life import GameOfLife
from gui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_grid(self, screen) -> None:
        for x, col in enumerate(self.life.field):
            for y, cell in enumerate(col):
                if cell:
                    screen.addstr(y + 1, x + 1, '#')
                else:
                    screen.addstr(y + 1, x + 1, ' ')

    def run(self) -> None:
        screen = curses.initscr()

        running = True
        while running:
            self.draw_grid(screen)
            running = self.life.step()
            screen.refresh()
        curses.endwin()


if __name__ == '__main__':
    game = Console(GameOfLife(64, 48))
    game.run()
