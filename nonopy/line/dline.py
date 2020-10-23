import numpy as np

from nonopy.cell import Cell

def __diffiter(new_line, old_line):
    for new, old in zip(new_line, old_line):
        yield new if old == Cell.EMPTY else Cell.EMPTY

def diff(new_line, old_line):
    dline = np.fromiter(__diffiter(new_line, old_line), Cell.dtype, len(new_line))
    has_any_diff = (dline != Cell.EMPTY).any()
    return dline, has_any_diff