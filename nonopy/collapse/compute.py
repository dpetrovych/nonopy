import numpy as np
from collections import namedtuple
from time import perf_counter_ns
from typing import List

from nonopy.cell import Cell, Cells, MIN_BLOCK_SPACE
from nonopy.combinations import calculate_hottask, calculate_moves, calculate_count
from nonopy.collapse.result import CollapseResult, reduce_collapsed
from nonopy.line.fieldline import FieldLine
from nonopy.line.taskline import TaskLine
from nonopy.metrics import Metrics

Task = List[int]
CollapseRun = namedtuple('CollapseRun', ['task', 'line'])


class Compute():
    def __init__(self, priority, collapser, metrics):
        self.priority = priority
        self.collapser = collapser
        self.metrics = metrics

    def __call__(self, task_line: TaskLine, field_line: FieldLine):
        """Performs collapse operation and returns diff with the line

        Args:
            field_line (FieldLine): represents current state of line on the field

        Returns:
            (nparray[int]): a new state of the line
        """
        start = perf_counter_ns()

        result = self.__collapse(task_line.task, field_line)
        task_line.count = result.count

        dt = perf_counter_ns() - start
        self.metrics.add_event(('collapse', task_line.id))
        self.metrics.add_value(('collapse.time', task_line.id), dt)

        return result.line

    def __collapse(self, task: Task, field_line: FieldLine):
        """Recursive function that calculates (collapses) all combinations of a segment of tasks 
            on a specific segment of field line.

        Args:
            task (Task): line task or a segment of the task
            field_line (FieldLine): line on the field or its continuos segment

        Returns:
            CollapsedResult: a new state of a line or its segment
        """
        def divide_by_crossed(x_start, x_end):
            self.metrics.add_event(('sub_collapse', 'divide_by_crossed'))

            def task_division(i):
                left_result, right_result, total_count = self.run_sides(
                    left=CollapseRun(task[:i], field_line[:x_start]),
                    right=CollapseRun(task[i:], field_line[x_end:]))

                if total_count == 0:
                    return None

                return CollapseResult.join(*left_result.line,
                                           *Cells.x(x_end - x_start),
                                           *right_result.line,
                                           count=total_count)

            division_results = (task_division(i)
                                for i in range(len(task), -1, -1))
            return reduce_collapsed(division_results, len(field_line))

        def divide_by_filled(f_start, f_end):
            self.metrics.add_event(('sub_collapse', 'divide_by_filled'))

            def task_division(block_index, block_pos):
                def bum(cond):
                    return MIN_BLOCK_SPACE if cond else 0

                block = task[block_index]
                block_end = block_pos + block
                left_bum = bum(block_index > 0)
                right_bum = bum(block_index < (len(task) - 1))

                left_edge = block_pos - left_bum
                right_edge = block_end + right_bum

                if (left_edge < 0 or right_edge > len(field_line) or
                    (field_line[left_edge:block_pos] == Cell.FILLED).any() or
                    (field_line[block_end:right_edge] == Cell.FILLED).any()):
                    return None

                left_result, right_result, total_count = self.run_sides(
                    left=CollapseRun(task[:block_index],
                                     field_line[:left_edge]),
                    right=CollapseRun(task[block_index + 1:],
                                      field_line[right_edge:]))

                if total_count == 0:
                    return None

                return CollapseResult.join(*left_result.line,
                                           *Cells.x(left_bum),
                                           *Cells.f(block),
                                           *Cells.x(right_bum),
                                           *right_result.line,
                                           count=total_count)

            blocks_placement = [(i, f_end - block, f_start)
                                for i, block in enumerate(task)
                                if block >= (f_end - f_start)]

            division_results = (task_division(i, pos)
                                for i, pos_start, pos_end in blocks_placement
                                for pos in range(pos_start, pos_end + 1))
            return reduce_collapsed(division_results, len(field_line))

        def inplace():
            self.metrics.add_event(('sub_collapse', 'inplace'))
            move_space = calculate_moves(task, len(field_line))
            if len(task) == 1 and move_space == 0:
                return CollapseResult.filled(len(field_line), 1)

            count = calculate_count(task, len(field_line))
            if move_space >= max(task):
                return CollapseResult.empty(len(field_line), count)

            def stack_left_ends():
                start = 0
                for block in task:
                    yield start + block
                    start += block + MIN_BLOCK_SPACE

            def stack_right_starts():
                start = move_space
                for block in task:
                    yield start
                    start += block + MIN_BLOCK_SPACE

            filled_indecies = [
                i
                for start, end in zip(stack_right_starts(), stack_left_ends())
                for i in range(start, end)
            ]

            line = np.full(len(field_line), Cell.EMPTY, Cell.dtype)
            line[filled_indecies] = Cell.FILLED
            return CollapseResult(line, count)

        if len(task) == 0 or (len(task) == 1 and task[0] == 0):
            return CollapseResult.crossed(len(field_line), 1)

        if (pos_x := field_line.find_center_crossed()) != (None, None):
            return divide_by_crossed(*pos_x)

        if (pos_f := field_line.find_center_filled()) != (None, None):
            return divide_by_filled(*pos_f)

        return inplace()

    def run_sides(self, *, left: CollapseRun, right: CollapseRun):
        """Runs left and right side ordered by priority class and returns both result if both sides have it

        Args:
            left (CollapseRun): left run tuple
            right (CollapseRun): right run tuple
        
        Returns:
            (CollapseResult, CollapseResult, int): left + right results and a combined combinations count
        """
        def should_run(task, field_line):
            """Allows run if only there is enough space to place blocks (has moves).
               Alternatively in task has no blocks - checks if field_line require at least 1 block.

            Args:
                task (list[int]): puzzle clues section
                field_line (FieldLine): state of line on the field or its section

            Returns:
                bool: should run continue for a specified side
            """
            if len(task) > 0:
                return calculate_moves(task, len(field_line)) >= 0
            else:
                return (field_line != Cell.FILLED).all()

        if (not should_run(left.task, left.line)
                or not should_run(right.task, right.line)):
            return None, None, 0

        lresult, rresult = None, None
        if self.priority.run_left_first(left, right):
            lresult = self.__collapse(left.task, left.line)
            if lresult is None:
                return None, None, 0

            rresult = self.__collapse(right.task, right.line)
            if rresult is None:
                return None, None, 0
        else:
            rresult = self.__collapse(right.task, right.line)
            if rresult is None:
                return None, None, 0

            lresult = self.__collapse(left.task, left.line)
            if lresult is None:
                return None, None, 0

        return lresult, rresult, lresult.count * rresult.count