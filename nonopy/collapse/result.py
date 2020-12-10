from collections.abc import Iterable
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


def reduce_collapsed(collapsed_results, length):
    '''Combine results from multiple divisions

    Args:
        combinations (Iterable[CollapsedResult]): iterable of all division results
        length (int): length of a line/section
    '''
    collapsed_results = [*filter(lambda result: result is not None, collapsed_results)]
    if len(collapsed_results) == 0:
        return None

    count = sum(l.count for l in collapsed_results)
    collapsed = np.array([l.line for l in collapsed_results], Cell.dtype)

    reduced = (Cell.FILLED if
               (column == Cell.FILLED).all() else Cell.CROSSED if
               (column == Cell.CROSSED).all() else Cell.EMPTY
               for column in collapsed.T)

    return CollapseResult(np.fromiter(reduced, Cell.dtype, length), count)
