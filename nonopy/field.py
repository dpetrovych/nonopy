import numpy as np

from nonopy.cell import Cell
from nonopy.format import format_grid


class Field:
    def __init__(self, height, width):
        self.grid = np.full((height, width), Cell.EMPTY, Cell.dtype)

    def __repr__(self):
        return format_grid(self.grid)

    is_solved = property(lambda self: (self.grid != Cell.EMPTY).all())

    def apply(self, order, index, line):
        if order == 'r':
            self.grid[index] = line
        elif order == 'c':
            self.grid[:, index] = line

    def apply_diff(self, order, index, diff):
        def merge(line):
            return [l if d == Cell.EMPTY else d for l, d in zip(line, diff)]

        if order == 'r':
            self.grid[index] = merge(self.grid[index])
        elif order == 'c':
            self.grid[:, index] = merge(self.grid[:, index])

    def get_line(self, order, index):
        if order == 'r':
            return self.grid[index]
        elif order == 'c':
            return self.grid[:, index]