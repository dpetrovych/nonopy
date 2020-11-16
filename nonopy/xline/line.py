import gc
import numpy as np

from nonopy.xline.combinations import can_be_filled, calculate_hottask, calculate, collapse, calculate_moves, calculate_count
from nonopy.cell import Cell, Cells, MIN_BLOCK_SPACE
from nonopy.xline.iter import not_none
from nonopy.format import format_line


class Line:
    def __init__(self, task, length):
        self.task = task
        self.length = length
        self.combinations = None
        self.count = calculate_count(task, length)
        self.init_hot = calculate_hottask(task, length)

    def collapse(self, field_line):
        """Performs collapse operation and returns diff with the line"""
        before_count = self.count

        collapsed, self.count = self.__sub_collapse(self.task, field_line)

        return collapsed, before_count

    def __sub_collapse(self, task, field_line):
        def reduce_collapsed(collapsed_lines):
            '''Combine results from multiple divisions
            Args:
                combinations (list[(nparray, int)])
            '''
            if len(collapsed_lines) == 0:
                return field_line.to_array(), 0

            count = sum(n for _, n in collapsed_lines)
            collapsed = np.array([col for col, _ in collapsed_lines],
                                 Cell.dtype)

            reduced = (Cell.FILLED if
                       (column == Cell.FILLED).all() else Cell.CROSSED if
                       (column == Cell.CROSSED).all() else Cell.EMPTY
                       for column in collapsed.T)

            return np.fromiter(reduced, Cell.dtype, len(field_line)), count

        def divide_by_crossed(x_index):
            left_line, left_l_n, left_r_n = field_line[:x_index].trim_x()
            right_line, right_l_n, right_r_n = field_line[x_index:].trim_x()

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

                seq = [
                    *Cells.x(left_l_n), *left_collapsed, *Cells.x(-left_r_n),
                    *Cells.x(right_l_n), *right_collapsed, *Cells.x(-right_r_n)
                ]

                return np.array(seq, Cell.dtype), total_count

            division_results = [
                *not_none(task_division(i) for i in range(len(task), -1, -1))
            ]

            return reduce_collapsed(division_results)

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

                left_collapsed, l_count = self.__sub_collapse(
                    left_task, left_line)
                right_collapsed, r_count = self.__sub_collapse(
                    right_task, right_line)

                total_count = l_count * r_count
                if total_count == 0:
                    return None

                seq = [
                    *left_collapsed, *Cells.x(left_bum), *Cells.f(block),
                    *Cells.x(right_bum), *right_collapsed
                ]

                return np.array(seq, Cell.dtype), total_count

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

            return reduce_collapsed(division_results)

        if len(task) == 0:
            return np.full(len(field_line), Cell.CROSSED, Cell.dtype), 1

        if (middle_x := field_line.find_center_x()) != None:
            return divide_by_crossed(middle_x)

        if (middle_f := field_line.find_center_filled()) != None:
            return divide_by_filled(middle_f)

        if calculate_hottask(task, len(field_line)):
            combs = calculate(task, len(field_line))
            return collapse(task, combs, len(field_line)), len(combs)
        else:
            return np.full(len(field_line), Cell.EMPTY,
                           Cell.dtype), calculate_count(task, len(field_line))
