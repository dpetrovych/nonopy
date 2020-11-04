import numpy as np

from nonopy.cell import Cell

def stoline(line: str):
    map = {
        '0': Cell.CROSSED,
        'x': Cell.CROSSED,
        '1': Cell.FILLED,
    }

    line = line.strip('|')
    imapped = (map.get(ch, Cell.EMPTY) for ch in line)
    return np.fromiter(imapped, Cell.dtype, len(line))


def emptyline(length: int):
    return np.full(length, Cell.EMPTY, Cell.dtype)
