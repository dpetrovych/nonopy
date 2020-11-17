import gc
import numpy as np
from typing import List

from nonopy.cell import Cell, Cells, MIN_BLOCK_SPACE
from nonopy.line.combinations import can_be_filled, calculate_hottask, calculate_moves, calculate_count
from nonopy.line.collapsed import CollapseResult, reduce_collapsed
from nonopy.line.iter import not_none
from nonopy.line.fieldline import FieldLine

Task = List[int]


class TaskLine:
    def __init__(self, task: Task, length: int):
        self.task = task
        self.length = length
        self.count = calculate_count(task, length)
        self.init_hot = calculate_hottask(task, length)

    def collapse(self, field_line: FieldLine):
        """Performs collapse operation and returns diff with the line"""
        before_count = self.count

        result = self.__sub_collapse(self.task, field_line)
        self.count = result.count

        return result.line, before_count

    def __sub_collapse(self, task: Task, field_line: FieldLine):
        def divide_by_crossed(x_index):
            left_line, left_l_n, left_r_n = field_line[:x_index].trim_x()
            right_line, right_l_n, right_r_n = field_line[x_index:].trim_x()

            def task_division(i):
                left_task, right_task = task[:i], task[i:]
                if (not can_be_filled(left_task, left_line)
                        or not can_be_filled(right_task, right_line)):
                    return None

                left_result = self.__sub_collapse(left_task, left_line)
                right_result = self.__sub_collapse(right_task, right_line)

                total_count = left_result.count * right_result.count
                if total_count == 0:
                    return None

                return CollapseResult.join(*Cells.x(left_l_n),
                                           *left_result.line,
                                           *Cells.x(-left_r_n),
                                           *Cells.x(right_l_n),
                                           *right_result.line,
                                           *Cells.x(-right_r_n),
                                           count=total_count)

            division_results = [
                *not_none(task_division(i) for i in range(len(task), -1, -1))
            ]

            return reduce_collapsed(division_results, field_line)

        def divide_by_filled(f_end):
            def task_division(block_index, block_pos):
                def bum(cond):
                    return MIN_BLOCK_SPACE if cond else 0

                block = task[block_index]
                block_end = block_pos + block
                left_bum = bum(block_index > 0)
                right_bum = bum(block_index < (len(task) - 1))

                left_edge = block_pos - left_bum
                right_edge = block_end + right_bum

                if (left_edge < 0 or right_edge > len(field_line)
                        or field_line[left_edge:block_pos] == Cell.FILLED
                        or field_line[block_end:right_edge] == Cell.FILLED):
                    return None

                left_task = task[:block_index]
                right_task = task[block_index + 1:]

                left_line = field_line[:left_edge]
                right_line = field_line[right_edge:]

                if (not can_be_filled(left_task, left_line)
                        or not can_be_filled(right_task, right_line)):
                    return None

                left_result = self.__sub_collapse(left_task, left_line)
                right_result = self.__sub_collapse(right_task, right_line)

                total_count = left_result.count * right_result.count
                if total_count == 0:
                    return None

                return CollapseResult.join(*left_result.line,
                                           *Cells.x(left_bum),
                                           *Cells.f(block),
                                           *Cells.x(right_bum),
                                           *right_result.line,
                                           count=total_count)

            f_start = f_end - 1
            while f_start > 0 and field_line[f_start - 1] == Cell.FILLED:
                f_start -= 1

            while f_end < len(field_line) and field_line[f_end] == Cell.FILLED:
                f_end += 1

            blocks_placement = [(i, f_end - block, f_start)
                                for i, block in enumerate(task)
                                if block >= (f_end - f_start)]

            division_results = [
                *not_none(
                    task_division(i, pos)
                    for i, pos_start, pos_end in blocks_placement
                    for pos in range(pos_start, pos_end + 1))
            ]

            return reduce_collapsed(division_results, field_line)

        def inplace():
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

        if (middle_x := field_line.find_center_crossed()) != None:
            return divide_by_crossed(middle_x)

        if (middle_f := field_line.find_center_filled()) != None:
            return divide_by_filled(middle_f)

        return inplace()
