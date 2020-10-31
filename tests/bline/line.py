from unittest import TestCase

import numpy as np

from nonopy.bline.line import Line
from nonopy.cell import Cell

class LineShould(TestCase):
    def assertArrayEqual(self, first, second):
        self.assertTrue((first == second).all(), msg = f"{first} != {second}")

    def test_collapse(self):
        line = Line([3, 1], 7)
        collapse, _ = line.collapse(np.full(7, Cell.EMPTY, Cell.dtype))

        self.assertArrayEqual(collapse, np.array([-1, -1, 1, -1, -1, -1, -1]))

    def test_filter__by_crossed(self):
        line = Line([3, 1], 7)
        field_line = np.array([-1, -1, -1, 0, -1, -1, 0])
        line.filter(field_line)
        collapse, _ = line.collapse(field_line)

        self.assertArrayEqual(collapse, np.array([1, 1, 1, 0, -1, -1, 0]))

    def test_filter__by_filled(self):
        line = Line([3, 1], 7)
        field_line = np.array([-1, 1, -1, -1, -1, -1, 1])
        line.filter(field_line)
        collapse, _ = line.collapse(field_line)

        self.assertArrayEqual(collapse, np.array([-1, 1, 1, -1, 0, 0, 1]))


