import numpy as np

from nonopy.line.fieldlinenorm import FieldLine
from nonopy.cell import Cell
from tests.testcase import TestCase


class FieldLineShould(TestCase):
    def test_trim_x_empty(self):
        trimmed, left, right = FieldLine([]).trim_x()

        self.assertArrayEqual(trimmed.to_array(), [])
        self.assertEquals(left, 0)
        self.assertEquals(right, 0)

    def test_trim_x_nothing(self):
        trimmed, left, right = FieldLine([-1, -1, 1]).trim_x()
        
        self.assertArrayEqual(trimmed.to_array(), [-1, -1, 1])
        self.assertEquals(left, 0)
        self.assertEquals(right, 0)

    def test_trim_x_left(self):
        trimmed, left, right = FieldLine([0, 0, -1, 1, -1]).trim_x()

        self.assertArrayEqual(trimmed.to_array(), [-1, 1, -1])
        self.assertEquals(left, 2)
        self.assertEquals(right, 0)

    def test_trim_x_right(self):
        trimmed, left, right = FieldLine([-1, 1, -1, 0, 0])[1:4].trim_x()

        self.assertArrayEqual(trimmed.to_array(), [1, -1])
        self.assertEquals(left, 0)
        self.assertEquals(right, -1)

    def test_trim_x_all(self):
        trimmed, left, right = FieldLine([0, 1, 0, -1, 0]).trim_x()

        self.assertArrayEqual(trimmed.to_array(), [1, 0, -1])
        self.assertEquals(left, 1)
        self.assertEquals(right, -1)

    def test_middle_crossed(self):
        line1 = FieldLine([-1, -1, -1, 0, -1])
        line2 = FieldLine([-1, -1, -1, 0])
        line3 = line1[1:4]
        middle1_x = line1.find_center_crossed()
        middle2_x = line2.find_center_crossed()
        middle3_x = line3.find_center_crossed()
        
        self.assertEquals(middle1_x, 4)
        self.assertEquals(middle2_x, 4)
        self.assertEquals(middle3_x, 3)

    def test_slice(self):
        line = FieldLine([-1, -1, 0, -1, -1])
        line_slice_l = line[:3]
        line_slice_r = line[2:]
        line_slice_m1 = line_slice_l[2:]
        line_slice_m2 = line_slice_r[:1]
        line_empty = line[3:3]
        
        self.assertArrayEqual(line_slice_l.to_array(), [-1, -1, 0])
        self.assertArrayEqual(line_slice_r.to_array(), [0, -1, -1])
        self.assertArrayEqual(line_slice_m1.to_array(), [0])
        self.assertArrayEqual(line_slice_m2.to_array(), [0])
        self.assertArrayEqual(line_empty.to_array(), [])
