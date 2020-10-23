from unittest import TestCase

import nonopy.line.cline as cline

class ClineShould(TestCase):
    def test_iter__simple_block(self):
        line = list(c for c in cline.iter([3], [1], 5))
        self.assertEqual([0, 1, 1, 1, 0], line)

    def test_iter__complex_block(self):
        line = list(cline.iter([1, 2, 1], [1, 1, 1], 9))
        self.assertEqual([0, 1, 0, 0, 1, 1, 0, 0, 1], line)

    def test_iter_single__full(self):
        line = list(cline.iter_single(5, 0, 5))
        self.assertEqual([1, 1, 1, 1, 1], line)

    def test_iter_single__short(self):
        line = list(cline.iter_single(3, 1, 5))
        self.assertEqual([0, 1, 1, 1, 0], line)
