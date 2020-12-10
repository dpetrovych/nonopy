import numpy as np
from typing import List

from nonopy.cell import Cell
from nonopy.line.fieldline import FieldLine


class CollapseResult:
    def __init__(self, line, count):
        '''Contains result of collapse operation

        Args:
            line (nparray): array with definitive cells
            count (int): number of combinations reduced in line
        '''
        self.line = line
        self.count = count

    @classmethod
    def join(cls, *array, count):
        return cls(np.array(array, Cell.dtype), count)

    @classmethod
    def empty(cls, length, count):
        return cls(np.full(length, Cell.EMPTY, Cell.dtype), count)

    @classmethod
    def crossed(cls, length, count):
        return cls(np.full(length, Cell.CROSSED, Cell.dtype), count)

    @classmethod
    def filled(cls, length, count):
        return cls(np.full(length, Cell.FILLED, Cell.dtype), count)
