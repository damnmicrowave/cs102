from typing import Tuple, List, Set, Optional
from random import randint


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """

    def text2underlined(text: str) -> str:
        return "\033[4m{}\033[0m".format(text)

    width = 2
    for row in range(9):
        line = ''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9))
        if str(row) in '25':
            line = text2underlined(line)
        print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [[values[j] for j in range(i, i + n)] for i in range(0, len(values), n)]


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [row[pos[1]] for row in grid]


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle01')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = (i // 3 * 3 for i in pos)
    return [grid[y][x] for y in range(row, row + 3) for x in range(col, col + 3)]


def find_empty_position(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле
    >>> find_empty_position([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_position([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_position([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if grid[y][x] == '.':
                return y, x
    return None


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значений для указанной позиции
    >>> grid = read_sudoku('puzzle01')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    return set('123456789') - set(get_col(grid, pos)) - set(get_row(grid, pos)) - set(get_block(grid, pos))


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle01')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_position(grid)
    if pos is None:
        return grid
    y, x = pos
    values = find_possible_values(grid, pos)
    if not values:
        return None
    for value in values:
        grid[y][x] = value
        solution = solve(grid)
        if check_solution(solution):
            return solution
        grid[y][x] = '.'


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    if solution is None:
        return False
    else:
        if '.' in [elem for row in solution for elem in row]:
            return False
    for c in range(9):
        if sum(get_row(solution, (c, c))) != 45 or sum(get_col(solution, (c, c))) != 45:
            return False
    for x in range(2):
        for y in range(2):
            if sum(get_block(solution, (x * 3, y * 3))) != 45:
                return False
    return True


def generate_sudoku(n: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    dots = 81 - min(max(0, n), 81)
    empty_grid = [['.' for _ in range(9)] for _ in range(9)]
    grid = solve(empty_grid)
    while dots:
        y, x = randint(0, 8), randint(0, 8)
        if grid[y][x] != '.':  # type: ignore
            grid[y][x] = '.'  # type: ignore
            dots -= 1
    return grid


if __name__ == '__main__':
    for fname in ['puzzle01', 'puzzle02', 'puzzle03']:
        puzzle_grid = read_sudoku(fname)
        display(puzzle_grid)
        puzzle_solution = solve(puzzle_grid)
        if not puzzle_solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(puzzle_solution)
