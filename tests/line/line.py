from unittest import TestCase
import numpy as np

from nonopy.line import Line
from nonopy.cell import Cell


def to_line(lst):
    return np.array(lst, Cell.dtype)

def empty_line(length):
    return np.full(length, Cell.EMPTY, Cell.dtype)

class LineShould(TestCase):
    def assertArrayEqual(self, first, second):
        self.assertTrue((first == second).all(), msg = f"{first} != {second}")

    def test_1block__empty_line(self):
        line = Line([3], 5)
        collapsed = line.collapse(empty_line(5))

        self.assertArrayEqual(collapsed, to_line([-1, -1, 1, -1, -1]))

    def test_2block__empty_line(self):
        line = Line([2, 1], 5)
        collapsed = line.collapse(empty_line(5))

        self.assertArrayEqual(collapsed, to_line([-1, 1, -1, -1, -1]))