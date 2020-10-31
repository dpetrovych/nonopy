from unittest import TestCase

import numpy as np

from nonopy.bline.block import Block

class BlockShould(TestCase):
    def assertArrayEqual(self, first, second):
        self.assertTrue((first == second).all(), msg = f"{first} != {second}")


    def test_2_blocks_rightleftmost(self):
        'line 3 1, width 7'
        block1, block2 = Block(3, 0, 2, 7), Block(1, 4, 2, 7)

        self.assertTrue(block1.is_leftmost)
        self.assertFalse(block1.is_rigthmost)
        self.assertTrue(block1.hot)

        self.assertTrue(block2.is_rigthmost)
        self.assertFalse(block2.is_leftmost)
        self.assertFalse(block2.hot)

    def test_1_block_rightleftmost(self):
        block1, block2 = Block(3, 0, 0, 3), Block(3, 0, 2, 5)

        self.assertTrue(block1.is_leftmost)
        self.assertTrue(block1.is_rigthmost)

        self.assertTrue(block2.is_rigthmost)
        self.assertTrue(block2.is_leftmost)


    def test_collapse(self):
        'line 3 1, width 7'
        block1, block2 = Block(3, 0, 2, 7), Block(1, 4, 2, 7)
        collapse1, collapse2 = block1.collapse(), block2.collapse()

        self.assertArrayEqual(collapse1, np.array([1./3, 2./3, 1, 2./3, 1./3, 0., 0.]))
        self.assertArrayEqual(collapse2, np.array([0, 0, 0, 0, 1./3, 1./3, 1./3]))

    def test_filter__by_crossed(self):
        'line 3 1, width 7'
        block1, block2 = Block(3, 0, 2, 7), Block(1, 4, 2, 7)
        field_line = np.array([-1, -1, -1, 0, -1, -1, 0])
        filtered1, filtered2 = (b.filter(field_line) for b in (block1, block2))

        self.assertEqual(filtered1, [True, False, False])
        self.assertEqual(filtered2, [True, True, False])

    def test_filter__by_filled(self):
        'line 3 1, width 7'
        block1, block2 = Block(3, 0, 2, 7), Block(1, 4, 2, 7)
        field_line = np.array([-1, 1, -1, -1, -1, 1, -1])
        filtered1, filtered2 = (b.filter(field_line) for b in (block1, block2))

        print(filtered1, filtered2)
        self.assertEqual(filtered1, [True, True, False])
        self.assertEqual(filtered2, [False, True, False])


