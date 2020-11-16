from unittest import TestCase
import numpy as np

from nonopy.line.fieldline import FieldLine
from nonopy.cell import Cell


class FieldLineShould(TestCase):
    def test_trim_x_empty(self):
        trimmed, left, right = FieldLine([]).trim_x()

        self.assertListEqual(trimmed.to_array(), [])
        self.assertEquals(left, 0)
        self.assertEquals(right, 0)

    def test_trim_x_nothing(self):
        trimmed, left, right = FieldLine([-1, -1, 1]).trim_x()

        self.assertListEqual(trimmed.to_array(), [-1, -1, 1])
        self.assertEquals(left, 0)
        self.assertEquals(right, 0)

    def test_trim_x_left(self):
        trimmed, left, right = FieldLine([0, 0, -1, 1, -1]).trim_x()

        self.assertListEqual(trimmed.to_array(), [-1, 1, -1])
        self.assertEquals(left, 2)
        self.assertEquals(right, 0)

    def test_trim_x_right(self):
        trimmed, left, right = FieldLine([-1, 1, -1, 0, 0]).trim_x()

        self.assertListEqual(trimmed.to_array(), [-1, 1, -1])
        self.assertEquals(left, 0)
        self.assertEquals(right, -2)

    def test_trim_x_all(self):
        trimmed, left, right = FieldLine([0, 1, 0, -1, 0]).trim_x()

        self.assertListEqual(trimmed.to_array(), [1, 0, -1])
        self.assertEquals(left, 1)
        self.assertEquals(right, -1)
