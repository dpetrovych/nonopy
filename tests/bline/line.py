from unittest import TestCase

import numpy as np

from nonopy.bline.line import Line
from nonopy.cell import Cell
from nonopy.format import format_line


def test(line: str):
    map = {
        '0': Cell.CROSSED,
        '1': Cell.FILLED,
    }

    line = line.strip('|')
    return np.fromiter((map.get(ch, Cell.EMPTY) for ch in line), Cell.dtype, len(line))


class LineShould(TestCase):
    def assertArrayEqual(self, first, second):
        self.assertEquals(len(first), len(second), msg=f'dimmentions missmatch')
        self.assertTrue((first == second).all(), msg=f"\n{format_line(first)} !=\n{format_line(second)}")

    def test_collapse(self):
        line = Line([3, 1], 7)
        collapse, _ = line.collapse()

        self.assertArrayEqual(collapse, test('|  1    |'))

    def test_filter_hard(self):
        line = Line([1, 8, 2, 2], 20)
        line.filter(test('|            1 0     |'))
        collapse, _ = line.collapse()

        self.assertArrayEqual(collapse, test('|      1111    0     |'))

    def test_filter_simple(self):
        line = Line([6, 2], 20)
        line.filter(test('|         111        |'))
        collapse, _ = line.collapse()

        self.assertArrayEqual(collapse, test('|000000              |'))

    def test_filter_harder(self):
        line = Line([2, 13, 23], 45)
        line.filter(test('| 11 1                                        |'))
        collapse, _ = line.collapse()

        self.assertArrayEqual(collapse, test('|011011111111111110    1111111111111111111    |'))

    def test_filter__by_crossed(self):
        line = Line([3, 1], 7)
        line.filter(test('|   0  0|'))
        collapse, _ = line.collapse()

        self.assertArrayEqual(collapse, np.array([1, 1, 1, 0, -1, -1, 0]))

    def test_filter__by_left_crossed_edge(self):
        line = Line([3, 1], 7)
        field_line = np.array([-1, 0, -1, -1, -1, -1, -1])
        line.filter(field_line)
        collapse, _ = line.collapse()

        self.assertArrayEqual(collapse, np.array([0, 0, 1, 1, 1, 0, 1]))

    def test_filter__by_right_crossed_edge(self):
        line = Line([3, 1], 7)
        field_line = np.array([-1, -1, -1, -1, -1, 0, 0])
        line.filter(field_line)
        collapse, _ = line.collapse()

        self.assertArrayEqual(collapse, np.array([1, 1, 1, 0, 1, 0, 0]))

    def test_filter__by_filled(self):
        line = Line([3, 1], 7)
        field_line = np.array([-1, 1, -1, -1, -1, -1, 1])
        line.filter(field_line)
        collapse, _ = line.collapse()

        self.assertArrayEqual(collapse, np.array([-1, 1, 1, -1, 0, 0, 1]))
