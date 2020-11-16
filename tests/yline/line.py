from nonopy.yline import Line
from nonopy.yline.fline import FieldLine
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

    def test_1block__emptyline(self):
        line = Line([3], 5)
        collapsed, _ = line.collapse(FieldLine(emptyline(5)))

        self.assertArrayEqual(collapsed, stoline('|  1  |'))

    def test_2block__emptyline(self):
        line = Line([2, 1], 5)
        collapsed, _ = line.collapse(FieldLine(emptyline(5)))

        self.assertArrayEqual(collapsed, stoline('| 1   |'))

    def test_2block__line_with_x(self):
        line = Line([2, 1], 6)
        collapsed, _ = line.collapse(FieldLine(stoline('|  00 0|')))

        self.assertArrayEqual(collapsed, stoline('|110010|'))

    def test_1block__line_with_x(self):
        line = Line([2], 20)
        collapsed, _ = line.collapse(
            FieldLine(stoline('|    xxxxxxxx  xxxxx |')))

        self.assertArrayEqual(collapsed, stoline('|    xxxxxxxx  xxxxxx|'))

    def test_4block_filter__line_with_x(self):
        line = Line([1, 8, 2, 2], 20)
        collapsed, _ = line.collapse(
            FieldLine(stoline('|            1 x     |')))

        self.assertArrayEqual(collapsed, stoline('|      1111  1 0     |'))

    def test_4block_filter__line_with_f(self):
        line = Line([3, 30, 1, 5], 45)
        collapsed, _ = line.collapse(
            FieldLine(
                stoline('|  1                                      1   |')))

        self.assertArrayEqual(
            collapsed,
            stoline('|  1    111111111111111111111111111      11   |'))

    def test_10block_filter__line_with_x(self):
        line = Line([4, 6, 1, 3, 2, 2, 3, 4, 1], 50)
        collapsed, _ = line.collapse(
            FieldLine(
                stoline(
                    '|xxxxx1111x111111x1 x111xxx11x11xx111x             |')))

        self.assertArrayEqual(
            collapsed,
            stoline('|xxxxx1111x111111x1xx111xxx11x11xx111x             |'))

    def test_8block_filter__886M_comb__line_with_x(self):
        line = Line([1, 2, 2, 1, 12, 1, 2, 2], 75)
        collapsed, before_count = line.collapse(FieldLine(stoline('|             x                    1 1  11                                  |')))

        self.assertArrayEqual(collapsed, stoline('|             x                    1 1  11                                  |'))
        self.assertEquals(before_count, 886322710)
        self.assertEquals(line.count, 177581035)
