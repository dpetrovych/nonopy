import gc
import numpy as np

import nonopy.line.cline as cline
import nonopy.zline.combinations as combinations
from nonopy.cell import Cell


class Line:
    def __init__(self, task, length):
        self.task = task
        self.length = length
        self.combinations = None
        self.count = combinations.calculate_count(task, length)
        self.init_hot = combinations.calculate_hottask(task, length)
    
    def collapse(self, line):
        """Performs collapse operation and returns diff with the line"""
        before_count = self.count

        combs = combinations.calculate(self.task, line)
        collapsed = combinations.collapse(self.task, combs, self.length)
        self.count = len(combs)

        return collapsed, before_count