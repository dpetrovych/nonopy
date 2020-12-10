from nonopy.combinations import calculate_count, calculate_hottask, calculate_moves
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

    def test_hottask(self):
        is_hot_3__5 = calculate_hottask([3], 5)
        is_hot_3__6 = calculate_hottask([3], 6)
        is_hot_2_1__5 = calculate_hottask([2, 1], 5)
        is_hot_2_1__6 = calculate_hottask([2, 1], 6)

        self.assertTrue(is_hot_3__5)
        self.assertFalse(is_hot_3__6)
        self.assertTrue(is_hot_2_1__5)
        self.assertFalse(is_hot_2_1__6)

    def test_moves(self):
        moves_3__5 = calculate_moves([3], 5)
        moves_3__6 = calculate_moves([3], 6)
        moves_2_1__5 = calculate_moves([2, 1], 5)
        moves_2_1__6 = calculate_moves([2, 1], 6)

        self.assertEqual(moves_3__5, 2)
        self.assertEqual(moves_3__6, 3)
        self.assertEqual(moves_2_1__5, 1)
        self.assertEqual(moves_2_1__6, 2)
        