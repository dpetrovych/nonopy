from nonopy.line.combinations import calculate_count
from nonopy.cell import Cell
from tests.testcase import TestCase


class CombinationsShould(TestCase):
    def test_count__1block(self):
        count_10_12 = calculate_count([10], 12)
        count_2_4 = calculate_count([2], 4)
        count_1_3 = calculate_count([1], 3)
        self.assertEqual(count_10_12, 3)
        self.assertEqual(count_2_4, 3)
        self.assertEqual(count_1_3, 3)

    def test_count__2block(self):
        count_2_2__6 = calculate_count([2, 2], 6)
        count_2_1__5 = calculate_count([2, 1], 5)
        count_1_1__4 = calculate_count([1, 1], 4)
        self.assertEqual(count_2_2__6, 3)
        self.assertEqual(count_2_1__5, 3)
        self.assertEqual(count_1_1__4, 3)

    def test_count__4block(self):
        count = calculate_count([6, 2, 16, 1], 35)
        self.assertEqual(count, 330)