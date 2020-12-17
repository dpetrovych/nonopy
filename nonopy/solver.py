import numpy as np
import textwrap as text
from typing import List, Tuple

from time import perf_counter_ns

from nonopy.line import TaskLine, FieldLine
from nonopy.cell import Cell
from nonopy.field import Field
from nonopy.fieldtrack import FieldTrack
from nonopy.hotheap import Hotheap
from nonopy.log import Log
from nonopy.linelookup import LineLookup
from nonopy.metrics import Metrics
from nonopy.collapse import Compute
from nonopy.combinations import calculate_count, calculate_hottask


class Solver():
    def __init__(self, collapse=None, metrics=None, log=None):
        self.metrics = metrics if metrics is not None else Metrics()
        self.log = log if log is not None else Log()
        self.collapse = collapse if collapse is not None else Compute(
            None, None, self.metrics)

    def __init_combinations(self, setup):
        """Generages all combinations counts for the puzzle. 
           Since calculating a count of combinations for each line may take considerable time 
           this action done separately and metrics are taken on each line.
        """
        def count(order, index, task, length):
            with self.log.init_line(order, index, task=task) as init_end:
                start = perf_counter_ns()

                line_id = order + str(index)
                count = calculate_count(task, length)

                dt = perf_counter_ns() - start
                self.metrics.add_event(('init', line_id))
                self.metrics.add_value(('init.time', line_id), dt)
                self.metrics.add_value(('complexity', line_id), count)

                init_end(count=count)
                return count

        rows = [
            count('r', i, row, setup.width) for i, row in enumerate(setup.rows)
        ]

        columns = [
            count('c', i, col, setup.height)
            for i, col in enumerate(setup.columns)
        ]

        return LineLookup(rows=rows, columns=columns)

    def __diff_collapse(
        self,
        order: str,
        index: int,
        task: List[int],
        count: int,
        line: FieldLine,
        baseline: FieldLine = None,
    ) -> Tuple[List[int], int]:
        """Runs collapse and returns line and combinations count difference

        Args:
            order (str): line order
            index (int): line index
            task (List[int]): line cues
            count (int): combinations count
            line (FieldLine): field line
            baseline (FieldLine): field line to compare on diff. Default: same as line

        Returns:
            Tuple[List[int], int]: line difference and combinations count difference
        """
        if baseline is None:
            baseline = line

        with self.log.collapse(order, index, task=task, line=line,
                               count=count) as log_collapse_end:
            collapsed_result = self.collapse(order, index, task, line)
            if collapsed_result is None:
                return None, None

            line_diff = baseline.diff(collapsed_result)
            count_diff = collapsed_result.count - count
            log_collapse_end(diff=line_diff)
        return (line_diff, count_diff)

    def solve(self, setup):
        """Solves puzzle in continuous reduction of blocks possitions

        Args:
            setup (Nonotask): a puzzle data

        Returns:
            (nparray): 2d puzzle grid as a numpy array
        """

        combinations = self.__init_combinations(setup)
        field = Field(setup.height, setup.width)

        tasks = LineLookup(
            rows=[TaskLine(row, setup.width) for row in setup.rows],
            columns=[TaskLine(col, setup.height) for col in setup.columns])

        def solve_hot(heap, track):
            """Allow recursively run solve with an initial/seeded heap

            Args:
                heap (Hotheap): initial/seeded heap
                track (FieldTrack): diff tracker

            Returns:
                (nparray|None): 2d puzzle grid as a numpy array or None if not solved
            """
            while True:
                # solve determined
                while heap.is_hot:
                    order, index = heap.pop()
                    field_line = field[order, index]
                    combinations_count = combinations[order, index]
                    task_line = tasks[order, index]

                    line_diff, count_diff = self.__diff_collapse(
                        order, index, task_line, combinations_count,
                        field_line)
                    
                    if line_diff is None:
                        return None

                    track.apply_diff(order, index, line_diff, count_diff)
                    heap.push_diff(order, line_diff)

                if field.is_solved:
                    return field.grid

                # solve non determined
                checkpoint = track.create_checkpoint()
                print('set', checkpoint)

                _, order, index = min((count, order, index)
                                      for order, lines in combinations
                                      for index, count in enumerate(lines)
                                      if count > 1)

                field_line = field[order, index]
                combinations_count = combinations[order, index]
                task_line = tasks[order, index]

                # Try seeding an empty cell as filled
                seed_index = field_line.find_center_cell(Cell.EMPTY)
                seeded_line = field_line.copy_with(seed_index, Cell.FILLED)

                print('seed - 1', order, index, seed_index)
                line_diff, count_diff = self.__diff_collapse(
                        order, index, task_line, combinations_count,
                        seeded_line, field_line)

                track.apply_diff(order, index, line_diff, count_diff)

                # Run recursively with a seeded heap
                seedheap = Hotheap(combinations, [])
                seedheap.push_diff(order, line_diff)
                result = solve_hot(seedheap, track)

                if result is not None:
                    return result

                # result is None - rollback progress
                _ = track.rollback(checkpoint)
                print('rollback', checkpoint)
                #TODO: log rollback

                # since solution in not found - cell is definitely CROSSED
                seeded_line = field_line.copy_with(seed_index, Cell.CROSSED)

                print('seed - 0', order, index, seed_index)
                line_diff, count_diff = self.__diff_collapse(
                        order, index, task_line, combinations_count,
                        seeded_line, field_line)
                
                track.apply_diff(order, index, line_diff, count_diff)
                heap.push_diff(order, line_diff)

            return field.grid if field.is_solved else None

        hot_list = [(order, index) for order, lines in tasks
                    for index, line in enumerate(lines)
                    if calculate_hottask(line.task, line.length)]

        track = FieldTrack(field, combinations)
        heap = Hotheap(combinations, hot_list)

        return solve_hot(heap, track)
