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
    def __init__(self, collapse=None, metrics=None, log=None):
        self.metrics = metrics if metrics is not None else Metrics()
        self.log = log if log is not None else Log()
        self.collapse = collapse if collapse is not None else Compute(None, None, self.metrics)

    def __init_line(self, order, index, task, length):
        """Creates a TaskLine object and keeps its metrics

        Args:
            order (str): character /[cr]/ that identifies the column or row order of a line
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

    def __init_combinations(self, task):
        """Generages all TaskLine objects for the puzzle. 
           Since calculating an count of combinations for each line may take considerable time 
           this action done separately and metrics are taken on each line.
        """
        return {
            'r': [
                self.__init_line('r', i, row, task.width)
                for i, row in enumerate(task.rows)
            ],
            'c': [
                self.__init_line('c', i, column, task.height)
                for i, column in enumerate(task.columns)
            ]
        }

    def solve(self, task):
        """Solves puzzle in continuous reduction of blocks possitions

        Returns:
            (nparray): 2d puzzle grid as a numpy array
        """

        field = Field(task.height, task.width)
        combinations = self.__init_combinations(task)
        heap = Hotheap(combinations)

        while heap.is_hot:
            order, index, task_line = heap.pop()
            field_line = FieldLine(field.get_line(order, index))

            with self.log.collapse(order,
                                   index,
                                   task=task_line,
                                   line=field_line) as log_collapse_end:
                collapsed_line = self.collapse(task_line, field_line)
                diff = field_line.diff(collapsed_line)
                log_collapse_end(diff=diff)

            field.apply(order, index, collapsed_line)
            heap.push_diff(order, diff)

        return field.grid if field.is_solved else None
