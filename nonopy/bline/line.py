import numpy as np
from itertools import accumulate

import nonopy.line.cline as cline
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
            [0] + task, lambda acc, cur: acc + cur + MIN_BLOCK_SPACE)

        self.blocks = [
            Block(block, start, move_space, length)
            for block, start in zip(task, start_indexes)
        ]

        self.init_hot = any(b.hot for b in self.blocks)

    def get_count(self):
        return np.prod(b.count for b in self.blocks)

    count = property(get_count)

    def collapse(self, line):
        """Performs collapse operation and returns diff with the line"""
        before_count = self.count
        collapsed = np.array([b.collapse() for b in self.blocks])

        print('b', self.blocks)
        print('c', collapsed)

        empty, filled = np.all(collapsed == 0, axis=0), np.any(collapsed == 1.,
                                                               axis=0)

        return np.full(len(line), -1) + 1 * empty + 2 * filled, before_count

    def filter(self, line):
        """Eliminates cobminations that do not correspond to current line state"""
        before_count = self.count
        for b in self.blocks:
            b.filter(line)

        return before_count, self.count