import numpy as np

import nonopy.line.dline as dline
from nonopy.line import Line
from nonopy.cell import Cell
from nonopy.field import Field
from nonopy.hotmap import Hotmap
from nonopy.log import Log
from nonopy.perf import PerfCounter


class Solver():
    def __init__(self, task, log=None):
        self.task = task
        self.status = None
        self.log = log if log else Log()
        self.perf = PerfCounter()
    
    def __repr__(self):
        return '\n'.join([f'status={self.status}', 'performance:', repr(self.perf)])

    def __init_combinations(self):
        self.hotmap = Hotmap()
        self.field = Field(self.task.height, self.task.width)
        self.combinations = {
            'r': [Line(row, self.task.width) 
                  for row in self.task.rows],
            'c': [Line(column, self.task.height) 
                  for column in self.task.columns]
        }

    def solve(self, explain = False):
        if self.status:
            raise Exception('solve already run')

        self.__init_combinations()
        
        self.perf.solve_begin()
        while True:
            lines_by_combinations = ((line.count, order, index, line) 
                for order, lines in self.combinations.items()
                for index, line in enumerate(lines))

            for count, order, index, line in sorted(lines_by_combinations):
                collapse_end = self.log.collapse_start(order, index, count=count)

                fline = self.field.get_line(order, index)
                nline = line.collapse(fline)
                diff, has_diff = dline.diff(nline, fline)

                collapse_end(diff)

                if not has_diff and self.hotmap.is_hot:
                    break
                
                self.field.apply(index, order, nline)
                self.hotmap.apply(index, order, diff)
            
            hotlines = self.hotmap.pop()
            if not hotlines:
                break

            for order, index in hotlines:
                line = self.combinations[order][index]
                count = line.count

                filter_end = self.log.filter_start(order, index, count=count)
                line.filter(self.field.get_line(order, index))
                filter_end(line.count)

        self.perf.solve_end()
        self.status, grid = ('solved', self.field.grid) if self.field.is_solved else ('unsolved', None)
        return grid
