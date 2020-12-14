import numpy as np
from typing import List


class TaskLine:
    def __init__(self, task: List[int], length: int):
        self.task = task
        self.length = length
