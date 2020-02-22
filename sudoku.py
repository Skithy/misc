import math
from timeit import default_timer as timer


class Sudoku:
    everything = set([i for i in range(1, 10)])

    def __init__(self):
        # Stores board data
        # Also stores data existing numbers for each row/column/grid for faster calculations
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.rows = [set() for _ in range(9)]
        self.columns = [set() for _ in range(9)]
        self.grids = [set() for _ in range(9)]

    def row(self, y: int):
        return self.rows[y]

    def column(self, x: int):
        return self.columns[x]

    def grid(self, x: int, y: int):
        grid_num = (math.floor(y / 3) * 3) + math.floor(x / 3)
        return self.grids[grid_num]

    def is_empty(self, x: int, y: int):
        return self.board[y][x] == None

    def get_available_moves(self, x: int, y: int):
        if not self.is_empty(x, y):
            return set()

        existing_moves = set()
        existing_moves.update(self.row(y), self.column(x), self.grid(x, y))
        return self.everything.difference(existing_moves)

    def get_next_move(self):
        best_move = None
        for y in range(9):
            for x in range(9):
                if sudoku.is_empty(x, y):
                    moves = sudoku.get_available_moves(x, y)
                    if best_move == None or len(moves) < len(best_move[2]):
                        best_move = (x, y, moves)

        return best_move

    def is_valid(self, x: int, y: int, value: int):
        if not self.is_empty(x, y):
            return False

        moves = self.get_available_moves(x, y)
        return value in moves

    def fill_cell(self, x: int, y: int, value: int):
        if not self.is_valid(x, y, value):
            raise Exception(f"({x}, {y}) {value} is not valid")

        self.board[y][x] = value
        self.row(y).add(value)
        self.column(x).add(value)
        self.grid(x, y).add(value)

    def remove_cell(self, x: int, y: int):
        if self.is_empty(x, y):
            raise Exception(f"({x}, {y}) is already empty")

        cell = self.board[y][x]
        self.row(y).remove(cell)
        self.column(x).remove(cell)
        self.grid(x, y).remove(cell)
        self.board[y][x] = None

    def parse_board(self, board_string: str):
        rows: List[str] = board_string.strip().split('\n')
        for y in range(9):
            for x in range(9):
                cell = rows[y][x]
                if cell.isnumeric():
                    self.fill_cell(x, y, int(cell))

    def print_board(self):
        row_string = ('+' + '-' * 3) * 3 + '+'

        for y in range(9):
            if y % 3 == 0:
                print(row_string)

            for x in range(9):
                if x % 3 == 0:
                    print('|', end='')
                cell = self.board[y][x]
                print('.' if cell is None else cell, end='')
            print('|')
        print(row_string)


def solver(sudoku):
    history = []

    def solve(sudoku):
        next_move = sudoku.get_next_move()
        if next_move == None:
            return True

        x, y, moves = next_move
        if len(moves) == 0:
            return False

        for move in moves:
            history.append((x, y, move))
            sudoku.fill_cell(x, y, move)

            if solve(sudoku):
                return True

            history.append((x, y, None))
            sudoku.remove_cell(x, y)

    if not solve(sudoku):
        print('Failed to find a solution.')

    return history

# Template
# board_string = """
# .........
# .........
# .........
# .........
# .........
# .........
# .........
# .........
# .........
# """

# Simple
# board_string = """
# ........8
# 978.4.13.
# .2....64.
# ..5.219..
# 137.9.286
# ..678.5..
# .43....2.
# .12.5.369
# 8........
# """


# Harder, with backtracking
board_string = """
...47....
5...6.73.
......219
.....59..
....26..1
..6.91.7.
4.7...5.8
........2
68.......
"""

sudoku = Sudoku()
sudoku.parse_board(board_string)

sudoku.print_board()

start = timer()
history = solver(sudoku)
end = timer()

elapsed = end - start
print(f"{elapsed} seconds, {len(history)} moves")

sudoku.print_board()
