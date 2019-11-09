import pygame
from pygame.locals import *
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
            width: int = 640,
            height: int = 480,
            cell_size: int = 10,
            speed: int = 10,
            max_generation = None
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        life = GameOfLife(self.width // self.cell_size, self.height // self.cell_size, max_generation)
        super().__init__(life)
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('#555555'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('#555555'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        black = pygame.Color('black')
        blue = pygame.Color('#00B2FF')
        for x in range(self.life.cell_width):
            for y in range(self.life.cell_height):
                cell = self.life.field[x][y]
                pygame.draw.rect(
                    self.screen,
                    blue if cell else black,
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('black'))
        self.draw_grid()
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = True
            self.draw_lines()
            pygame.display.flip()
            running = self.life.step()
            self.draw_grid()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    game = GUI(max_generation=10)
    game.run()
