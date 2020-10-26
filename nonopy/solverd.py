import numpy as np
import textwrap as text

import nonopy.line.dline as dline
from nonopy.line import Line
from nonopy.cell import Cell
from nonopy.field import Field
from nonopy.hotheap import Hotheap
from nonopy.log import Log
from nonopy.perf import PerfCounter
from nonopy.metrics import Metrics


class Solver():
    def __init__(self, task, log=None):
        self.task = task
        self.status = None
        self.log = log if log else Log()
        self.perf = PerfCounter()
    
    def __repr__(self):
        return '\n'.join([f'status = {self.status}', 
                           'metrics:', text.indent(repr(self.metrics), '  '), 
                           'performance:', text.indent(repr(self.perf), '  ')])

    def __init_combinations(self):
        self.field = Field(self.task.height, self.task.width)
        self.combinations = {
            'r': [Line(row, self.task.width) 
                  for row in self.task.rows],
            'c': [Line(column, self.task.height) 
                  for column in self.task.columns]
        }

        self.heap = Hotheap(self.combinations)
        self.metrics = Metrics(self.combinations)

    def solve(self, explain = False):
        if self.status:
            raise Exception('solve already run')

        with self.perf.init():
            self.__init_combinations()

        with self.perf.solve():
            while self.heap.is_hot:
                self.metrics.inc_cycle()
                
                order, index, line = self.heap.pop()

                log_filter_end = self.log.filter_start(order, index, count=line.count)
                n_lines_in, n_lines_out = line.filter(self.field.get_line(order, index))

                self.metrics.add_line_instantiation('filter', n_lines_in)
                log_filter_end(n_lines_out)

                log_collapse_end = self.log.collapse_start(order, index, count=line.count)

                field_line = self.field.get_line(order, index)
                collapsed_line, n_lines_in = line.collapse(field_line)
                diff, _ = dline.diff(collapsed_line, field_line)

                self.metrics.add_line_instantiation('collapse', n_lines_in)
                log_collapse_end(diff)
                
                self.field.apply(order, index, collapsed_line)
                self.heap.push_diff(order, diff)

        self.status, grid = ('solved', self.field.grid) if self.field.is_solved else ('unsolved', None)
        return grid
