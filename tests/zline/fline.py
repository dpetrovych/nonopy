from unittest import TestCase
import numpy as np

from nonopy.zline.fline import trim_x
from nonopy.cell import Cell


class FlineShould(TestCase):
    def test_trim_x_empty(self):
        trimmed, left, right = trim_x([])

        self.assertListEqual(trimmed, [])
        self.assertEquals(left, 0)
        self.assertEquals(right, 0)

    def test_trim_x_nothing(self):
        trimmed, left, right = trim_x([-1, -1, 1])

        self.assertListEqual(trimmed, [-1, -1, 1])
        self.assertEquals(left, 0)
        self.assertEquals(right, 0)

    def test_trim_x_left(self):
        trimmed, left, right = trim_x([0, 0, -1, 1, -1])

        self.assertListEqual(trimmed, [-1, 1, -1])
        self.assertEquals(left, 2)
        self.assertEquals(right, 0)

    def test_trim_x_right(self):
        trimmed, left, right = trim_x([-1, 1, -1, 0, 0])

        self.assertListEqual(trimmed, [-1, 1, -1])
        self.assertEquals(left, 0)
        self.assertEquals(right, -2)

    def test_trim_x_all(self):
        trimmed, left, right = trim_x([0, 1, 0, -1, 0])

        self.assertListEqual(trimmed, [1, 0, -1])
        self.assertEquals(left, 1)
        self.assertEquals(right, -1)
