from unittest import TestCase
import numpy as np

from nonopy.line.combinations import calculate_count, calculate
from nonopy.cell import Cell

def to_line(lst):
    return np.array(lst, Cell.dtype)

def empty_line(length):
    return to_line([Cell.EMPTY] * length)

class CombinationsShould(TestCase):
    def test_calculate_count(self):
        subtests = [
            ([3], 3, 1),
            ([1, 1], 3, 1),
            ([1, 1], 4, 3),
            ([1, 2, 1], 8, 10)
        ]

        for task, length, expected in subtests:
            with self.subTest('calculate_count', task = task, length = length):
                count = calculate_count(task, length)
                self.assertEqual(expected, count)

    def test_calculate__empty_line(self):
        subtests = [
            ([3], empty_line(3), [[0]]),
            ([1, 1], empty_line(3), [[0, 0]]),
            ([1, 1], empty_line(4), [[0, 0], [0, 1], [1, 0]]), 
            ([1, 2, 1], empty_line(8), [[0, 0, 0], [0, 0, 1], [0, 0, 2], 
                                        [0, 1, 0], [0, 1, 1], [0, 2, 0], 
                                        [1, 0, 0], [1, 0, 1], [1, 1, 0], 
                                        [2, 0, 0]])
        ]

        for task, line, expected in subtests:
            with self.subTest('test_calculate__empty_line', task = task, line = line):
                combinations = calculate(task, line)
                self.assertListEqual(expected, combinations)

    def test_calculate__filled_line(self):
        subtests = [
            ([1], to_line([0, -1, 0]), [[1]]),
            ([1], to_line([-1, -1, 1]), [[2]]),
            ([1, 1], to_line([-1, 0, -1, -1]), [[0, 0], [0, 1]]),
            ([1, 2, 1], empty_line(8), [[0, 0, 0], [0, 0, 1], [0, 0, 2], 
                                        [0, 1, 0], [0, 1, 1], [0, 2, 0], 
                                        [1, 0, 0], [1, 0, 1], [1, 1, 0], 
                                        [2, 0, 0]])
        ]

        for task, line, expected in subtests:
            with self.subTest('test_calculate__filled_line', task = task, line = line):
                combinations = calculate(task, line)
                self.assertListEqual(expected, combinations)
