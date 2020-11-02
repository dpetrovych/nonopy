import numpy as np
from itertools import accumulate
from functools import reduce

from nonopy.bline.block import Block
from nonopy.cell import Cell

MIN_BLOCK_SPACE = 1


class Line:
    def __init__(self, task, length):
        self.task = task
        self.length = length

        move_space = length - sum(
            task) - MIN_BLOCK_SPACE * len(task) + MIN_BLOCK_SPACE
        start_indexes = accumulate(
            task, lambda acc, cur: acc + cur + MIN_BLOCK_SPACE, initial=0)

        self.blocks = [
            Block(block, start, move_space, length)
            for block, start in zip(task, start_indexes)
        ]

        self.init_hot = any(b.hot for b in self.blocks)

    def get_count(self):
        return reduce(lambda prod, b: prod * b.count, self.blocks, 1)

    count = property(get_count)

    def collapse(self):
        """Performs collapse operation and returns diff with the line"""
        before_count = self.count
        collapsed = np.array([b.collapse() for b in self.blocks])

        crossed = np.all(collapsed == 0, axis=0)
        filled = np.any(collapsed == 1., axis=0)

        return (np.full(self.length, Cell.EMPTY) +
                (Cell.CROSSED - Cell.EMPTY) * crossed +
                (Cell.FILLED - Cell.EMPTY) * filled), before_count

    def filter(self, line):
        """Eliminates cobminations that do not correspond to current line state"""
        before_count = self.count

        # filter each
        reduce(lambda _, block: block.filter(line), self.blocks, None)

        # compact left
        reduce(lambda l, block: block.filter_left(l), self.blocks, 0)

        # compact right
        reduce(lambda r, block: block.filter_right(r), self.blocks[::-1], 0)

        return before_count, self.count