from nonopy.line import TaskLine, FieldLine
from nonopy.cell import Cell
from nonopy.metrics import Metrics
from tests.testcase import TestCase
from tests.utils import stoline, fline


class TaskLineShould(TestCase):
    def test_init_hot(self):
        metrics = Metrics()
        line_3_5, line_3_6 = TaskLine('c1', [3], 5, metrics), TaskLine('c2', [3], 6, metrics)
        line_2_1_5, line_2_1_6 = TaskLine('r1', [2, 1], 5, metrics), TaskLine('r2', [2, 1], 6, metrics)

        self.assertTrue(line_3_5.init_hot)
        self.assertFalse(line_3_6.init_hot)
        self.assertTrue(line_2_1_5.init_hot)
        self.assertFalse(line_2_1_6.init_hot)

    def test_1block__emptyline(self):
        line = TaskLine('c1', [3], 5, Metrics())
        collapsed = line.collapse(fline('|     |'))

        self.assertArrayEqual(collapsed, stoline('|  1  |'))

    def test_2block__emptyline(self):
        line = TaskLine('c1', [2, 1], 5, Metrics())
        collapsed = line.collapse(fline('|     |'))

        self.assertArrayEqual(collapsed, stoline('| 1   |'))

    def test_2block__line_with_x(self):
        line = TaskLine('c1', [2, 1], 6, Metrics())
        collapsed = line.collapse(fline('|  00 0|'))

        self.assertArrayEqual(collapsed, stoline('|110010|'))

    def test_1block__line_with_x(self):
        line = TaskLine('c1', [2], 20, Metrics())
        collapsed = line.collapse(fline('|    xxxxxxxx  xxxxx |'))

        self.assertArrayEqual(collapsed, stoline('|    xxxxxxxx  xxxxxx|'))

    def test_4block_filter__line_with_x(self):
        line = TaskLine('c1', [1, 8, 2, 2], 20, Metrics())
        collapsed = line.collapse(fline('|            1 x     |'))

        self.assertArrayEqual(collapsed, stoline('|      1111  1 0     |'))

    def test_4block_filter__line_with_f(self):
        line = TaskLine('c1', [3, 30, 1, 5], 45, Metrics())
        collapsed = line.collapse(
            fline('|  1                                      1   |'))

        self.assertArrayEqual(
            collapsed,
            stoline('|  1    111111111111111111111111111      11   |'))

    def test_10block_filter__line_with_x(self):
        line = TaskLine('c1', [4, 6, 1, 3, 2, 2, 3, 4, 1], 50, Metrics())
        collapsed = line.collapse(
            fline('|xxxxx1111x111111x1 x111xxx11x11xx111x             |'))

        self.assertArrayEqual(
            collapsed,
            stoline('|xxxxx1111x111111x1xx111xxx11x11xx111x             |'))

    def test_8block_filter__886M_comb__line_with_x(self):
        line = TaskLine('c1', [1, 2, 2, 1, 12, 1, 2, 2], 75, Metrics())
        collapsed = line.collapse(
            fline(
                '|             x                    1 1  11                                  |'
            ))

        self.assertArrayEqual(
            collapsed,
            stoline(
                '|             x                    1 1  11                                  |'
            ))
        self.assertEqual(line.count, 177581035)
        
