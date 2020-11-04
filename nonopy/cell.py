import numpy
"""Minimal space between 2 blocks"""
MIN_BLOCK_SPACE = 1


class Cell:
    EMPTY = -1
    CROSSED = 0
    FILLED = 1

    dtype = numpy.int8

    @staticmethod
    def is_not_empty(cell):
        return cell != Cell.EMPTY
