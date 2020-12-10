from nonopy.line import TaskLine, FieldLine
from nonopy.cell import Cell
from nonopy.metrics import Metrics
from tests.testcase import TestCase
from tests.utils import stoline, fline


class TaskLineShould(TestCase):
    def test_init_hot(self):
        line_3_5, line_3_6 = TaskLine('c1', [3], 5), TaskLine('c2', [3], 6)
        line_2_1_5, line_2_1_6 = TaskLine('r1', [2, 1],
                                          5), TaskLine('r2', [2, 1], 6)

        self.assertTrue(line_3_5.init_hot)
        self.assertFalse(line_3_6.init_hot)
        self.assertTrue(line_2_1_5.init_hot)
        self.assertFalse(line_2_1_6.init_hot)
