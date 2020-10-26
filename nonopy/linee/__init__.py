import numpy as np

import nonopy.linee.cline as cline
import nonopy.linee.combinations as combinations
from nonopy.cell import Cell

class Line:
    def __init__(self, task, length):
        self.task = task
        self.length = length
        self.combinations = None
        self.init_count = combinations.calculate_count(task, length)
        self.init_hot = combinations.calculate_hottask(task, length)

    def get_count(self):
        return len(self.combinations) if self.combinations else self.init_count
    
    count = property(get_count)

    def collapse(self, line):
        """Performs collapse operation and returns diff with the line"""
        before_count = self.count
        if not self.combinations:
            self.combinations = combinations.calculate(self.task, line)

        return combinations.collapse(self.task, self.combinations, self.length), before_count

    def filter(self, line):
        """Eliminates cobminations that do not correspond to current line state"""
        before_count = self.count
        self.combinations = (combinations.filter(self.task, self.combinations, line)
            if self.combinations else combinations.calculate(self.task, line))
        
        return before_count, self.count