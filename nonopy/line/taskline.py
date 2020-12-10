import numpy as np
from collections import namedtuple
from time import perf_counter_ns
from typing import List

from nonopy.cell import Cell, Cells, MIN_BLOCK_SPACE
from nonopy.combinations import calculate_hottask, calculate_count

Task = List[int]

class TaskLine:
    def __init__(self, id: str, task: Task, length: int):
        self.id = id
        self.task = task
        self.length = length
        self.count = calculate_count(task, length)
        self.init_hot = calculate_hottask(task, length)
