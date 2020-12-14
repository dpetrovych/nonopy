from nonopy.field import Field
from nonopy.linelookup import LineLookup

class FieldTrack:
    def __init__(self, field : Field, combinations: LineLookup):
        self.field = field
        self.combinations = combinations
        self.log = []
        self.checkpoints = []
    

    def apply_diff(self, order, index, line_diff, count_diff):
        self.log.append((order, index, line_diff, count_diff))
        self.field.apply_diff(order, index, line_diff)
        self.combinations[order, index] += count_diff