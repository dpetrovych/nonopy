import numpy as np

from nonopy.cell import Cell
from nonopy.format import format_grid
from nonopy.line.fieldline import FieldLine


class Field:
    """Represents a puzzle grid and gives access to individual lines"""
    def __init__(self, height, width):
        self.grid = np.full((height, width), Cell.EMPTY, Cell.dtype)

    def __repr__(self):
        return format_grid(self.grid)

    is_solved = property(lambda self: (self.grid != Cell.EMPTY).all())

    def apply_diff(self, order, index, diff):
        """Sets diff cells on to the field line

        Args:
            order (str): 'r' (row) or 'c' (column)
            index (int): 0-based line index
            diff (nparray): 1d array represents new cells
        """
        def merge(line):
            return [l if d is None else d for l, d in zip(line, diff)]

        if order == 'r':
            self.grid[index] = merge(self.grid[index])
        elif order == 'c':
            self.grid[:, index] = merge(self.grid[:, index])
        else:
            raise ValueError(f'Unknown order value: {order}')

    def __getitem__(self, key):
        """Gets a copy of a field line

        Args:
            key (Tuple[str, int]): order and index of a line

        Returns:
            FieldLine: a type decorating a field line
        """
        order, index = key
        line = self.__get_line_slice(order, index).copy()
        line.setflags(write=0)
        return FieldLine(line)

    def __get_line_slice(self, order, index):
        if order == 'r':
            return self.grid[index]

        if order == 'c':
            return self.grid[:, index]

        raise ValueError(f'Unknown order value: {order}')
