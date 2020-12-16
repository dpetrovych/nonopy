from heapq import heappush, heappop, heapify
from typing import List, Tuple

import numpy as np

from nonopy.cell import Cell
from nonopy.linelookup import LineLookup


def get_opposite_order(order):
    if order == 'c':
        return 'r'
    if order == 'r':
        return 'c'
    raise ValueError(f'Unknown order value: {order}')


class Hotheap:
    def __init__(self, combinations: LineLookup, hot_list: List[Tuple[str, int]]):
        """Initializes heap of lines ready to be collapsed. Sorted asc by combinations count.

        Args:
            combinations (LineLookup): A puzzle field
            hot_list (List[Tuple[str, int]]): List of order and index of lines, which yield results when collapsed 
        """
        self.combinations = combinations
        self.sets = dict((order, set(i for o, i in hot_list if o == order))
                         for order in ['c', 'r'])

        self.heap = [(self.combinations[order, index], order, index)
                     for order, index in hot_list]
        heapify(self.heap)

    is_hot = property(lambda self: len(self.heap) > 0)

    def push_diff(self, order: str, diff):
        """Sets an opposite lines for non-empty cells in diff as hot

        Args:
            order (str): order of the diff line
            diff (nparray): array of diff cells
        """
        effected_cells = {i for i, d in enumerate(diff) if d is not None}
        if not effected_cells:
            return

        op_order = get_opposite_order(order)
        for index in effected_cells - self.sets[op_order]:
            count = self.combinations[op_order, index]
            heappush(self.heap, (count, op_order, index))
            self.sets[op_order].add(index)

    def pop(self):
        """Gets next hot (order, index) pair with minimal combinations count

        Returns:
            Tuple[str, int]: (order, index) pair
        """
        try:
            _, order, index = heappop(self.heap)
            self.sets[order].remove(index)
            return order, index
        except IndexError:
            return None, None
