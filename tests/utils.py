import numpy as np

from nonopy.cell import Cell
from nonopy.line import FieldLine


def stoline(line: str):
    map = {
        '0': Cell.CROSSED,
        'x': Cell.CROSSED,
        '1': Cell.FILLED,
    }

    line = line.strip('|')
    imapped = (map.get(ch, Cell.EMPTY) for ch in line)
    return np.fromiter(imapped, Cell.dtype, len(line))

def fline(line: str):
    return FieldLine(stoline(line))
