class Cell:
    def __init__(self, walkable: bool, coords: (int, int), damage=0, symbol='0', prev_cell=None) -> None:
        self.walkable = walkable
        self.symbol = symbol
        if walkable:
            self.distance_from_start = 0
            self.cost = 0

            self.coords = coords
            self.prev_cell = prev_cell
            self.damage = damage

    def __bool__(self):
        return self.walkable

    def __eq__(self, other) -> bool:
        return self.coords == other.coords


class Maze:
    def __init__(self, health: int) -> None:
        self.map = dict()
        self.width = 0
        self.height = 0
        self.start_cell = None
        self.target_cell = None
        self.walkable = []
        self.checked = []
        self.health = health

    def load_map(self, filename='map') -> None:
        with open(filename) as file:
            data = file.read()
            print(data)
            for y, row in enumerate(data.split('\n')):
                self.height = y + 1
                for x, elem in enumerate(row.split()):
                    self.width = x + 1
                    if elem == 'S':
                        self.start_cell = Cell(True, (x, y), 0, elem)
                        self.map[x, y] = self.start_cell
                        self.walkable.append(self.start_cell)
                    elif elem == 'T':
                        self.target_cell = Cell(True, (x, y), 0, elem)
                        self.map[x, y] = self.target_cell
                    elif elem == '#':
                        self.map[x, y] = Cell(False, (x, y), symbol=elem)
                    else:
                        self.map[x, y] = Cell(True, (x, y), int(elem), elem)

    def get_path(self) -> list:
        path = []
        curr_cell = self.target_cell
        while curr_cell is not None:
            path.append(curr_cell.coords)
            curr_cell = curr_cell.prev_cell
        return path[::-1]

    def print_path(self, path: list) -> None:
        if not path:
            print('\nPath not found')
            return
        output = '\n'
        for y in range(self.height):
            for x in range(self.width):
                output += '█ ' if (x, y) in path else f'{self.map[x, y].symbol} '
            output += '\n'
        print(output)

    def calculate_path(self):
        while len(self.walkable):

            curr_cell = self.walkable[0]  # type: Cell
            index = 0
            for i, cell in enumerate(self.walkable):  # type: int, Cell
                if cell.cost < curr_cell.cost:
                    curr_cell = cell
                    index = i

            self.walkable.pop(index)
            self.checked.append(curr_cell)

            if curr_cell == self.target_cell:
                return self.get_path()

            neighbours = []
            for dx, dy in (0, -1), (0, 1), (-1, 0), (1, 0):
                x, y = curr_cell.coords
                cell = self.map.get((x + dx, y + dy), Cell(False, (0, 0)))
                if not cell or cell in self.checked or cell in self.walkable:
                    continue
                cell.prev_cell = curr_cell
                neighbours.append(cell)

            for cell in neighbours:
                cell.distance_from_start = curr_cell.distance_from_start + 1
                x, y = cell.coords
                tx, ty = self.target_cell.coords
                estimated_distance = (x - tx) ** 2 + (y - ty) ** 2
                cell.cost = cell.distance_from_start + estimated_distance
                if self.health - cell.damage > 0:
                    self.walkable.append(cell)


if __name__ == '__main__':
    maze = Maze(3)
    maze.load_map()
    result = maze.calculate_path()
    maze.print_path(result)
