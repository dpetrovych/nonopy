import numpy as np
from itertools import repeat

from nonopy.cell import Cell


class Block:
    def __init__(self, block_length, start, move_space, line_length):
        self.block_length = block_length
        self.line_length = line_length
        self.start = start
        self.moves = list(repeat(True, move_space + 1))

        self.is_leftmost = self.start == 0
        self.is_rigthmost = self.start + self.block_length + move_space == self.line_length

    def __repr__(self):
        return f'Block(length={self.block_length}, start={self.start}, count={self.count})'

    count = property(lambda self: sum(self.moves))
    hot = property(lambda self: sum(self.moves) <= self.block_length)

    def collapse(self):
        mask = np.zeros(self.line_length, dtype=np.int64)
        available_moves = np.where(self.moves)[0]
        for move in available_moves:
            start = self.start + move
            mask[start:start + self.block_length] += 1

        return mask / len(available_moves)

    def filter(self, field_line):
        def is_valid(move):
            start, end = self.start + move, self.start + move + self.block_length
            edgel = range(move) if self.is_leftmost else [start - 1]
            edger = range(end,
                          self.line_length) if self.is_rigthmost else [end]

            body = (field_line[start:end] != Cell.CROSSED).all()
            left = (field_line[edgel] != Cell.FILLED).all()
            right = (field_line[edger] != Cell.FILLED).all()

            return body and left and right

        self.moves = [
            is_available and is_valid(move)
            for move, is_available in enumerate(self.moves)
        ]

        return self.moves

    def filter_left(self, leftmost):
        if leftmost > 0:
            self.moves[:leftmost] = repeat(False, leftmost)

        return np.where(self.moves)[0][0]

    def filter_right(self, rightmost):
        if rightmost > 0:
            self.moves[-rightmost:] = repeat(False, rightmost)

        return len(self.moves) - np.where(self.moves)[0][-1] - 1
