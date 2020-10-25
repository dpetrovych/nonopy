import numpy as np
import textwrap as text

import nonopy.line.dline as dline
from nonopy.line import Line
from nonopy.cell import Cell
from nonopy.field import Field
from nonopy.hotmap import Hotmap
from nonopy.log import Log
from nonopy.perf import PerfCounter
from nonopy.metrics import Metrics
from nonopy.ticktack import ticktack


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
        self.hotmap = Hotmap()
        self.field = Field(self.task.height, self.task.width)
        self.combinations = {
            'r': [Line(row, self.task.width) 
                  for row in self.task.rows],
            'c': [Line(column, self.task.height) 
                  for column in self.task.columns]
        }

        self.metrics = Metrics(self.combinations)

    def solve(self, explain = False):
        if self.status:
            raise Exception('solve already run')

        self.__init_combinations()
        self.perf.solve_begin()
            
        ticktackiter, breaker = ticktack('r', 'c')
        for direction in ticktackiter():
            self.metrics.inc_cycle()

            # hotmap combinations filter
            hotlines = self.hotmap.pop()
            max_count = None
            for order, index in hotlines:
                line = self.combinations[order][index]
                log_filter_end = self.log.filter_start(order, index, count=line.count)
                n_lines_in, n_lines_out = line.filter(self.field.get_line(order, index))

                max_count = max_count if max_count and max_count > n_lines_out else n_lines_out
                self.metrics.add_line_instantiation('filter', n_lines_in)
                log_filter_end(n_lines_out)
            
            # field combinations colapse
            lines_by_combinations = ((line.count, index, line) 
                for index, line in enumerate(self.combinations[direction]))

            for count, index, line in sorted(lines_by_combinations):
                log_collapse_end = self.log.collapse_start(direction, index, count=count)

                field_line = self.field.get_line(direction, index)
                collapsed_line, n_lines_in = line.collapse(field_line)
                diff, has_diff = dline.diff(collapsed_line, field_line)

                self.metrics.add_line_instantiation('collapse', n_lines_in)
                log_collapse_end(diff)

                if not has_diff and self.hotmap.is_hot and not (max_count and n_lines_in <= max_count):
                    break
                
                self.field.apply(direction, index, collapsed_line)
                self.hotmap.apply(direction, index, diff)

            breaker(not self.hotmap.is_hot)

        self.perf.solve_end()
        self.status, grid = ('solved', self.field.grid) if self.field.is_solved else ('unsolved', None)
        return grid
