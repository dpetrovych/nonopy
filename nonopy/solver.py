import numpy as np
import textwrap as text

from time import perf_counter_ns

from nonopy.line import TaskLine, FieldLine
from nonopy.cell import Cell
from nonopy.field import Field
from nonopy.hotheap import Hotheap
from nonopy.log import Log
from nonopy.metrics import Metrics
from nonopy.collapse import Compute


class Solver():
    def __init__(self, task, collapse=None, log=None):
        self.task = task
        self.status = None
        self.metrics = Metrics()
        self.log = log if log is not None else Log()
        self.collapse = collapse if collapse is not None else Compute(
            None, None, self.metrics)

    def __repr__(self):
        return '\n'.join([f'status = {self.status}'])

    def __init_line(self, order, index, task, length):
        """Creates a TaskLine object and keeps its metrics

        Args:
            order (str): character /[cr]/ that indentifies the column or row order of a line
            index (int): 0-based index of line in an order
            task (list[int]): list of puzzle cues for the order/index
            length (int): length of a line in the specified order

        Returns:
            TaskLine
        """

        with self.log.init_line(order, index, task=task) as init_end:
            start = perf_counter_ns()

            line_id = order + str(index)
            line = TaskLine(line_id, task, length)

            dt = perf_counter_ns() - start
            self.metrics.add_event(('init', line_id))
            self.metrics.add_value(('init.time', line_id), dt)
            self.metrics.add_value(('complexity', line_id), line.count)

            init_end(count=line.count)
            return line

    def preheat(self):
        """Generages all TaskLine objects for the puzzle. 
           Since calculating an count of combinations for each line may take considerable time 
           this action done separately and metrics are taken on each line.
        """
        self.field = Field(self.task.height, self.task.width)
        self.combinations = {
            'r': [
                self.__init_line('r', i, row, self.task.width)
                for i, row in enumerate(self.task.rows)
            ],
            'c': [
                self.__init_line('c', i, column, self.task.height)
                for i, column in enumerate(self.task.columns)
            ]
        }

        self.heap = Hotheap(self.combinations)
        self.status = 'hot'

    def solve(self):
        """Solves puzzle in continious reduction of blocks possitions

        Returns:
            (nparray): 2d puzzle grid as a numpy array
        """
        if not self.status:
            self.preheat()

        if not self.status == 'hot':
            Exception('solve already run')

        while self.heap.is_hot:
            order, index, task_line = self.heap.pop()
            field_line = FieldLine(self.field.get_line(order, index))

            with self.log.collapse(order, index, task=task_line, line=field_line) as log_collapse_end:
                collapsed_line = self.collapse(task_line, field_line)
                diff = field_line.diff(collapsed_line)
                log_collapse_end(diff=diff)

            self.field.apply(order, index, collapsed_line)
            self.heap.push_diff(order, diff)

        self.status, grid = ('solved',
                             self.field.grid) if self.field.is_solved else (
                                 'unsolved', None)
        return grid
