import numpy as np
from itertools import chain
from heapq import heappush, heappop, heapify

from nonopy.cell import Cell


def reverse_order(v):
    if v == 'c':
        return 'r'
    if v == 'r':
        return 'c'
    raise ValueError("order parameter should be 'c'|'r'")


class Hotheap:
    def __init__(self, combinations):
        self.combinations = combinations
        self.heap = [(line.count, order, index)
                     for order, lines in self.combinations.items()
                     for index, line in enumerate(lines) if line.init_hot]

        heapify(self.heap)

        self.sets = dict(
            (order, set(i for _, o, i in self.heap if o == order))
            for order in ['c', 'r'])

    is_hot = property(lambda self: len(self.heap) > 0)

    def push_diff(self, order, diff):
        effected_cells = set(np.where(diff != Cell.EMPTY)[0])
        if not effected_cells:
            return

        r_order = reverse_order(order)
        for index in effected_cells - self.sets[r_order]:
            line = self.combinations[r_order][index]
            heappush(self.heap, (line.count, r_order, index))
            self.sets[r_order].add(index)

    def pop(self):
        try:
            _, order, index = heappop(self.heap)
            self.sets[order].remove(index)
            return order, index, self.combinations[order][index]
        except IndexError:
            return None, None, None
