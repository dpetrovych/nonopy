from nonopy.zline.combinations import calculate
from nonopy.cell import Cell
from tests.testcase import TestCase
from tests.utils import stoline, emptyline


class CombinationsShould(TestCase):
    def test_1block__emptyline(self):
        combinations = calculate([3], emptyline(5))
        self.assertEqual(combinations, [[0], [1], [2]])

    def test_2block__emptyline(self):
        combinations = calculate([2, 1], emptyline(5))
        self.assertEqual(combinations, [[0, 0], [0, 1], [1, 0]])

    def test_1block__line_with_x(self):
        combinations = calculate([2], stoline('|    xxxxxxxx  xxxxx |'))
        self.assertEquals(combinations, [[0], [1], [2], [12]])

    def test_2block__line_with_x(self):
        combinations = calculate([2, 1], stoline('|  00 0|'))
        self.assertArrayEqual(combinations, [[0, 1]])

    def test_4block_filter__line_with_x(self):
        combinations = calculate([1, 8, 2, 2],
                                 stoline('|            1 x     |'))
        self.assertEquals(
            combinations,
            [[0, 0, 0, 1], [0, 0, 0, 2], [0, 0, 0, 3], [0, 0, 0, 4],
             [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 1, 2], [0, 0, 1, 3],
             [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 0, 2], [0, 1, 0, 3],
             [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 0, 2], [1, 0, 0, 3],
             [0, 3, 1, 0], [0, 4, 0, 0], [1, 2, 1, 0], [1, 3, 0, 0],
             [2, 1, 1, 0], [2, 2, 0, 0], [3, 0, 1, 0], [3, 1, 0, 0],
             [4, 0, 0, 0]])