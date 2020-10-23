import numpy as np

from nonopy.cell import Cell

def apply(line, diff):
    return [idiff if idiff != Cell.EMPTY else iline
            for iline, idiff in zip(line, diff)]


class Field:
    def __init__(self, height, width):
        self.grid = np.full((height, width), Cell.EMPTY, Cell.dtype)
    
    def get_is_solved(self):
        return all(Cell.is_not_empty(cell) for cell in self.grid)

    is_solved = property(get_is_solved)

    def apply(self, index, order, diff):
        if order == 'r':
            self.grid[index] = apply(self.grid[index], diff)
        elif order == 'c':
            self.grid[:, index] = apply(self.grid[:, index], diff)
    
    def get_line(self, order, index):
        if order == 'r':
            return self.grid[index]
        elif order == 'c':
            return self.grid[:, index]