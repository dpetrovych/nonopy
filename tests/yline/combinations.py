from nonopy.xline.combinations import calculate
from nonopy.cell import Cell
from tests.testcase import TestCase
from tests.utils import stoline, emptyline


class CombinationsShould(TestCase):
    def test_1block__emptyline(self):
        combinations = calculate([3], 5)
        self.assertEqual(combinations, [[0], [1], [2]])

    def test_2block__emptyline(self):
        combinations = calculate([2, 1], 5)
        self.assertEqual(combinations, [[0, 0], [0, 1], [1, 0]])