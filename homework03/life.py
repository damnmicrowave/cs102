import json
from random import randint


class GameOfLife:

    def __init__(self, cell_width=64, cell_height=48, max_generation=None) -> None:
        self.field = None
        self.prev_field = None
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.max_generation = max_generation
        self.curr_generation = 0
        self.field = self.create_grid(randomize=True)

    def create_grid(self, randomize: bool = False):
        return [[randint(0, 1) if randomize else 0 for _ in range(self.cell_height)] for _ in range(self.cell_width)]

    def get_neighbours(self, cell):
        x, y = cell
        return [self.field[x + dx][y + dy] for dy in range(-1, 2) for dx in range(-1, 2) if
                (dy != 0 or dx != 0) and 0 <= x + dx < self.cell_width and 0 <= y + dy < self.cell_height]

    def get_next_generation(self):
        new_field = list()
        for x, col in enumerate(self.field):
            new_field.append([])
            for y, cell in enumerate(col):
                neighbours = self.get_neighbours((x, y))
                new_cell = 0
                if sum(neighbours) == 3 and not cell:
                    new_cell = 1
                elif 1 < sum(neighbours) < 4 and cell:
                    new_cell = 1
                new_field[x].append(new_cell)
        return new_field

    def step(self) -> bool:
        self.prev_field = self.field
        self.field = self.get_next_generation()
        self.curr_generation += 1
        if self.max_generation is not None:
            return not self.is_max_generations_exceeded
        return self.is_changing

    def toggle_cell(self, pos):
        x, y = pos
        cell = self.field[x][y]
        self.field[x][y] = 0 if cell else 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.curr_generation >= self.max_generation

    @property
    def is_changing(self) -> bool:
        return self.field != self.prev_field

    def from_file(self, filename, name) -> None:
        with open(filename) as file:
            self.field = json.load(file)[name]

    def save(self, filename, name) -> None:
        with open(filename, 'w+') as file:
            saved_data = json.load(file) if file.read() != '' else {}
            saved_data[name] = self.field
            json.dump(saved_data, file)
