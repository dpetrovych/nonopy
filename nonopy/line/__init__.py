import numpy as np

import nonopy.line.cline as cline
import nonopy.line.combinations as combinations
from nonopy.cell import Cell

class Line:
    def __init__(self, task, length):
        self.task = task
        self.length = length
        self.combinations = None
        self.init_count = combinations.calculate_count(task, length)

    def get_count(self):
        return len(self.combinations) if self.combinations else self.init_count
    
    count = property(get_count)

    def collapse(self, line):
        """Performs collapse operation and returns diff with the line"""
        if not self.combinations:
            self.combinations = combinations.calculate(self.task, line)

        return combinations.collapse(self.task, self.combinations, self.length)

    def filter(self, line):
        """Eliminates cobminations that do not correspond to current line state"""
        before = self.count
        self.combinations = (combinations.filter(self.task, self.combinations, line)
            if self.combinations else combinations.calculate(self.task, line))
        
        return before, self.count