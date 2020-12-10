import numpy as np

from nonopy.line.fieldline import FieldLine
from nonopy.cell import Cell
from tests.testcase import TestCase


class FieldLineShould(TestCase):
    def test_middle_crossed(self):
        line1 = FieldLine([-1, -1, -1, 0, -1])
        line2 = FieldLine([-1, -1, -1, 0])
        line3 = line1[1:4]
        middle1_x = line1.find_center_crossed()
        middle2_x = line2.find_center_crossed()
        middle3_x = line3.find_center_crossed()
        
        self.assertEqual(middle1_x, (3, 4))
        self.assertEqual(middle2_x, (3, 4))
        self.assertEqual(middle3_x, (2, 3))

    def test_slice(self):
        line = FieldLine([-1, -1, 0, -1, -1])
        line_slice_l = line[:3]
        line_slice_r = line[2:]
        line_slice_m1 = line_slice_l[2:]
        line_slice_m2 = line_slice_r[:1]
        line_empty = line[3:3]
        
        self.assertArrayEqual(line_slice_l, [-1, -1, 0])
        self.assertArrayEqual(line_slice_r, [0, -1, -1])
        self.assertArrayEqual(line_slice_m1, [0])
        self.assertArrayEqual(line_slice_m2, [0])
        self.assertArrayEqual(line_empty, [])
