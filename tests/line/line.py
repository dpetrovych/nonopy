import numpy as np

from nonopy.line import Line
from nonopy.cell import Cell
from tests.testcase import TestCase
from tests.utils import stoline, emptyline


class LineShould(TestCase):
    def test_init_hot(self):
        line_3_5, line_3_6 = Line([3], 5), Line([3], 6)

        line_2_1_5, line_2_1_6 = Line([2, 1], 5), Line([2, 1], 6)

        self.assertTrue(line_3_5.init_hot)
        self.assertFalse(line_3_6.init_hot)
        self.assertTrue(line_2_1_5.init_hot)
        self.assertFalse(line_2_1_6.init_hot)

    def test_1block__empty_line(self):
        line = Line([3], 5)
        collapsed, _ = line.collapse(emptyline(5))

        self.assertArrayEqual(collapsed, stoline('  1  '))

    def test_2block__empty_line(self):
        line = Line([2, 1], 5)
        collapsed, _ = line.collapse(emptyline(5))

        self.assertArrayEqual(collapsed, stoline(' 1   '))

    def test_4block_filter__line_with_x(self):
        line = Line([1, 8, 2, 2], 20)
        line.filter(stoline('|            1 x     |'))

        self.assertEquals(
            line.combinations,
            [[0, 0, 0, 1], [0, 0, 0, 2], [0, 0, 0, 3], [0, 0, 0, 4],
             [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 1, 2], [0, 0, 1, 3],
             [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 0, 2], [0, 1, 0, 3],
             [0, 3, 1, 0], [0, 4, 0, 0], [1, 0, 0, 0], [1, 0, 0, 1],
             [1, 0, 0, 2], [1, 0, 0, 3], [1, 2, 1, 0], [1, 3, 0, 0],
             [2, 1, 1, 0], [2, 2, 0, 0], [3, 0, 1, 0], [3, 1, 0, 0],
             [4, 0, 0, 0]])
