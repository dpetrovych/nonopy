import numpy as np
from typing import List

from nonopy.cell import Cell
from nonopy.line.fieldline import FieldLine


class CollapseResult:
    def __init__(self, line, count):
        '''Contains result of collapse operation
        Args:
            line  - array with definitive cells
            count - number of combinations reduced in line
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

    @classmethod
    def none(cls, line):
        return cls(line, 0)


def reduce_collapsed(collapsed_lines: List[CollapseResult],
                     field_line: FieldLine):
    '''Combine results from multiple divisions
    Args:
        combinations (list[(nparray, int)])
    '''
    if len(collapsed_lines) == 0:
        return CollapseResult.none(field_line.to_array())

    count = sum(l.count for l in collapsed_lines)
    collapsed = np.array([l.line for l in collapsed_lines], Cell.dtype)

    reduced = (Cell.FILLED if
               (column == Cell.FILLED).all() else Cell.CROSSED if
               (column == Cell.CROSSED).all() else Cell.EMPTY
               for column in collapsed.T)

    return CollapseResult(np.fromiter(reduced, Cell.dtype, len(field_line)),
                          count)
