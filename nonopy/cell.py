import numpy
import itertools as it
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


class Cells:
    @staticmethod
    def x(n):
        '''Iterator of n crossed cells'''
        return it.repeat(Cell.CROSSED, n)

    @staticmethod
    def f(n):
        '''Iterator of n filled cells'''
        return it.repeat(Cell.FILLED, n)
