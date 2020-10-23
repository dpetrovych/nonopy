from itertools import chain

from nonopy.cell import Cell

class Hotmap:
    def __init__(self):
        self.columns = {}
        self.rows = {}
    
    def apply(self, index, order, diff):
        effected_cells = {i for i, cell in enumerate(diff) if cell != Cell.EMPTY}
        if order == 'r':
            self.columns |= effected_cells
        elif order == 'c':
             self.rows |= effected_cells
        else:
            raise ValueError("order parameter should be 'c'|'r'")
    
    def pop(self):
        hotlines = [chain((('c', c) for c in self.columns), (('r', r) for r in self.rows))]
        self.columns, self.rows = {}, {}
        return hotlines