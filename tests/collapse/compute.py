from nonopy.line import TaskLine, FieldLine
from nonopy.cell import Cell
from nonopy.collapse import Compute
from nonopy.collapse.reducer import SlimReducer
from nonopy.collapse.priority import RecursionPriority
from nonopy.metrics import Metrics
from tests.testcase import TestCase
from tests.utils import stoline, fline


class ComputeShould(TestCase):
    def get_compute(self):
        return Compute(RecursionPriority(), SlimReducer(), Metrics())

    def test_1block__emptyline(self):
        line = TaskLine([3], 5)
        compute = self.get_compute()

        collapsed = compute('c', 0, line, fline('|     |'))

        self.assertArrayEqual(collapsed.line, stoline('|  1  |'))

    def test_2block__emptyline(self):
        line = TaskLine([2, 1], 5)
        compute = self.get_compute()

        collapsed = compute('c', 0, line, fline('|     |'))

        self.assertArrayEqual(collapsed.line, stoline('| 1   |'))

    def test_2block__line_with_x(self):
        line = TaskLine([2, 1], 6)
        compute = self.get_compute()

        collapsed = compute('c', 0, line, fline('|  00 0|'))

        self.assertArrayEqual(collapsed.line, stoline('|110010|'))

    def test_1block__line_with_x(self):
        line = TaskLine([2], 20)
        compute = self.get_compute()

        collapsed = compute('c', 0, line, fline('|    xxxxxxxx  xxxxx |'))

        self.assertArrayEqual(collapsed.line,
                              stoline('|    xxxxxxxx  xxxxxx|'))

    def test_4block_filter__line_with_x(self):
        line = TaskLine([1, 8, 2, 2], 20)
        compute = self.get_compute()

        collapsed = compute('c', 0, line, fline('|            1 x     |'))

        self.assertArrayEqual(collapsed.line,
                              stoline('|      1111  1 0     |'))

    def test_4block_filter__line_with_f(self):
        line = TaskLine([3, 30, 1, 5], 45)
        compute = self.get_compute()

        collapsed = compute('c', 0, 
            line, fline('|  1                                      1   |'))

        self.assertArrayEqual(
            collapsed.line,
            stoline('|  1    111111111111111111111111111      11   |'))

    def test_10block_filter__line_with_x(self):
        line = TaskLine([4, 6, 1, 3, 2, 2, 3, 4, 1], 50)
        compute = self.get_compute()

        collapsed = compute('c', 0, 
            line,
            fline('|xxxxx1111x111111x1 x111xxx11x11xx111x             |'))

        self.assertArrayEqual(
            collapsed.line,
            stoline('|xxxxx1111x111111x1xx111xxx11x11xx111x             |'))

    def test_8block_filter__886M_comb__line_with_x(self):
        line = TaskLine([1, 2, 2, 1, 12, 1, 2, 2], 75)
        compute = self.get_compute()

        collapsed = compute('c', 0, 
            line,
            fline(
                '|             x                    1 1  11                                  |'
            ))

        self.assertArrayEqual(
            collapsed.line,
            stoline(
                '|             x                    1 1  11                                  |'
            ))

        self.assertEqual(collapsed.count, 177581035)
