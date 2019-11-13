import pygame as pg
from life import GameOfLife
import abc


class UI(abc.ABC):

    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        pass


class GUI(UI):

    def __init__(
            self,
            life: GameOfLife,
            width: int = 640,
            height: int = 480,
            cell_size: int = 10,
            speed: int = 10,
    ) -> None:
        super().__init__(life)

        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen = pg.display.set_mode((width, height))
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pg.draw.line(self.screen, pg.Color('#222222'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pg.draw.line(self.screen, pg.Color('#222222'), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        black = pg.Color('black')
        blue = pg.Color('#00B2FF')
        for x in range(self.life.cell_width):
            for y in range(self.life.cell_height):
                cell = self.life.field[x][y]
                pg.draw.rect(
                    self.screen,
                    blue if cell else black,
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                )

    def run(self) -> None:
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption('Game of Life')
        self.screen.fill(pg.Color('black'))
        self.draw_grid()
        running = True
        paused = False
        while running:
            if not paused:
                running = self.life.step()
            for event in pg.event.get():
                pressed_keys = pg.key.get_pressed()
                if event.type == pg.QUIT:
                    running = False
                elif pressed_keys[pg.K_SPACE]:
                    paused = not paused
                elif event.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()
                    self.life.toggle_cell((x // self.cell_size, y // self.cell_size))
                elif pressed_keys[pg.K_s]:
                    paused = True
                    self.life.save('saved_data.json', input('Enter save name: '))
                elif pressed_keys[pg.K_l]:
                    paused = True
                    self.life.from_file('saved_data.json', input('Enter save name: '))
            self.draw_lines()
            pg.display.flip()
            self.draw_grid()
            clock.tick(self.speed)
        pg.quit()


if __name__ == '__main__':
    game = GUI(GameOfLife())
    game.run()
