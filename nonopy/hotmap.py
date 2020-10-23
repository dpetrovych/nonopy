import numpy as np
from itertools import chain

from nonopy.cell import Cell

class Hotmap:
    def __init__(self):
        self.columns = set()
        self.rows = set()
    
    is_hot = property(lambda self: self.columns or self.rows)

    def apply(self, index, order, diff):
        effected_cells = set(np.where(diff != Cell.EMPTY)[0])
        if not effected_cells:
            return

        if order == 'r':
            self.columns |= effected_cells
        elif order == 'c':
             self.rows |= effected_cells
        else:
            raise ValueError("order parameter should be 'c'|'r'")
    
    def pop(self):
        hotlines = [*chain((('c', c) for c in self.columns), (('r', r) for r in self.rows))]
        self.columns, self.rows = set(), set()
        return hotlines