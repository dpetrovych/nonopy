import numpy as np
from itertools import chain

from nonopy.line import Line
import nonopy.line.dline as dline
from nonopy.cell import Cell
from nonopy.field import Field
from nonopy.hotmap import Hotmap
from nonopy.log import Log


class Solver():
    def __init__(self, task):
        self.task = task
        self.status = '-'
    
    def __repr__(self):
        return f'Field:\n{self.field}]\nStatus: {self.status}'

    def __init_combinations(self):
        self.log = Log()
        self.hotmap = Hotmap()
        self.field = Field(self.task.height, self.task.width)
        self.combinations = {
            'r': [Line(row, self.task.width) 
                  for row in self.task.rows],
            'c': [Line(column, self.task.height) 
                  for column in self.task.columns]
        }

    def solve(self, explain = False):
        self.__init_combinations()

        while True:
            lines_by_combinations = ((line.count, order, index, line) 
                for order, lines in self.combinations
                for index, line in enumerate(lines))

            for count, order, index, line in sorted(lines_by_combinations):
                self.log.begin_collapse(order, index, count=count)

                fline = self.field.get_line(order, index)
                diff, has_result = dline.diff(line.collapse(fline), fline)
                
                self.log.diff(order, index, diff=diff)
                if not has_result:
                    break

                self.hotmap.apply(index, order, diff)
            
            hotlines = self.hotmap.pop()
            if not hotlines:
                break

            for order, index in hotlines:
                line = self.combinations[order][index]
                count_before, count_after = line.filter(self.field.get_line(order, index))
                self.log.filter(order, index, count_before=count_before, count_after=count_after)
                

        self.status, grid = ('solved', self.field.grid) if self.field.is_solved else ('unsolved', None)
        return grid
