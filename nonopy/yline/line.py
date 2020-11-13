import gc
import numpy as np
import itertools as it

import nonopy.yline.combinations as combinations
from nonopy.yline.fline import find_center_x, trim_x
from nonopy.cell import Cell
from nonopy.yline.iter import not_none
from nonopy.format import format_line


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

        collapsed, self.count = self.__sub_collapse(self.task, line)

        return collapsed, before_count

    def __sub_collapse(self, task, line):
        def divide_by_x(x_index):
            left_line, left_l_n, left_r_n = trim_x(line[:x_index])
            right_line, right_l_n, right_r_n = trim_x(line[x_index:])

            def can_be_filled(tsk, ln):
                if len(tsk) > 0:
                    return combinations.calculate_moves(tsk, len(ln)) >= 0
                else:
                    return (ln != Cell.FILLED).all()

            def task_division(i):
                left_task, right_task = task[:i], task[i:]
                if (not can_be_filled(left_task, left_line)
                        or not can_be_filled(right_task, right_line)):
                    return None

                left_collapsed, l_count = self.__sub_collapse(
                    left_task, left_line)
                right_collapsed, r_count = self.__sub_collapse(
                    right_task, right_line)

                total_count = l_count * r_count
                if total_count == 0:
                    return None

                def x(n):
                    '''Iterator of n crossed cells'''
                    return it.repeat(Cell.CROSSED, n)

                seq = [
                    *x(left_l_n), *left_collapsed, *x(-left_r_n),
                    *x(right_l_n), *right_collapsed, *x(-right_r_n)
                ]

                return np.array(seq, Cell.dtype), total_count

            task_collapse_combinations = [
                *not_none(task_division(i) for i in range(len(task), -1, -1))
            ]

            if len(task_collapse_combinations) == 0:
                return line, 0

            count = sum(n for _, n in task_collapse_combinations)
            collapsed = np.array(
                [col for col, _ in task_collapse_combinations], Cell.dtype)

            reduced = (Cell.FILLED if
                       (column == Cell.FILLED).all() else Cell.CROSSED if
                       (column == Cell.CROSSED).all() else Cell.EMPTY
                       for column in collapsed.T)

            return np.fromiter(reduced, Cell.dtype, len(line)), count

        if len(task) == 0:
            return np.full(len(line), Cell.CROSSED, Cell.dtype), 1

        if (middle_x := find_center_x(line)) != None:
            return divide_by_x(middle_x)

        combs = combinations.calculate(task, line)
        if len(combs) == 0:
            return line, 0

        return combinations.collapse(task, combs, len(line)), len(combs)