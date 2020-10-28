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
        self.metrics = Metrics()
    
    def __repr__(self):
        return '\n'.join([f'status = {self.status}', 
                           'metrics:', text.indent(repr(self.metrics), '  '), 
                           'performance:', text.indent(repr(self.perf), '  ')])

    def __init_line(self, order, index, task, length):
        with self.log.init_line(order, index, task = task) as init_end:
            line = Line(task, length)
            init_end(count = line.count)
            return line

    def preheat(self):
        with self.perf.init():
            self.field = Field(self.task.height, self.task.width)
            self.combinations = {
                'r': [self.__init_line('r', i, row, self.task.width)
                    for i, row in enumerate(self.task.rows)],
                'c': [self.__init_line('c', i, column, self.task.height)
                    for i, column in enumerate(self.task.columns)]
            }

            self.heap = Hotheap(self.combinations)
            self.metrics.set_comlexity(self.combinations)
        
        self.status = 'hot'

    def solve(self):
        if not self.status:
            self.preheat()
        
        if not self.status == 'hot':
            Exception('solve already run')

        with self.perf.solve():
            while self.heap.is_hot:
                self.metrics.inc_cycle()
                
                order, index, line = self.heap.pop()
                field_line = self.field.get_line(order, index)

                with self.log.filter(order, index, count=line.count) as log_filter_end:
                    n_lines_in, n_lines_out = line.filter(field_line)

                    self.metrics.add_line_instantiation('filter', n_lines_in)
                    log_filter_end(count_after=n_lines_out)

                with self.log.collapse(order, index, count=line.count) as log_collapse_end:
                    collapsed_line, n_lines_in = line.collapse(field_line)
                    diff, _ = dline.diff(collapsed_line, field_line)

                    self.metrics.add_line_instantiation('collapse', n_lines_in)
                    log_collapse_end(diff = diff)
                
                self.field.apply(order, index, collapsed_line)
                self.heap.push_diff(order, diff)

        self.status, grid = ('solved', self.field.grid) if self.field.is_solved else ('unsolved', None)
        return grid
