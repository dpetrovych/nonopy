import numpy as np
from itertools import islice, tee

from nonopy.cell import Cell, MIN_BLOCK_SPACE
from nonopy.format import format_line
import nonopy.line.cline as cline
from nonopy.yline.task import find_weight_center


def calculate_moves(task, length):
    return length - sum(task) - MIN_BLOCK_SPACE * len(task) + MIN_BLOCK_SPACE


def calculate_hottask(task, length):
    """Calculates if task has block that produces filled cells on collapse on a clean line"""
    max_block = max(task)
    return calculate_moves(task, length) < max_block


def can_be_filled(task, field_line):
    if len(task) > 0:
        return calculate_moves(task, len(field_line)) >= 0
    else:
        return (field_line != Cell.FILLED).all()


def __iderivative(iterator, start=0):
    prev = start
    for item in iterator:
        yield item - prev
        prev = item


def calculate_count(task, length):
    """
    Calculates how many combinations of spans (thus block positions) available for a specific task for a line length
    Helps to prioritize reduce operations before calculating actual spans

    Uses divide & conquer strategy by dividing line in 2 and calculating respective counts in left and right parts.
    Than assembles results by multiplying.
    
    """
    if len(task) == 1:
        return length - task[0] + 1

    center, (minl, minr) = find_weight_center(task)
    maxl = length - minr

    left_task, right_task = task[:center], task[center:]

    right_cursor = lambda cl: length - cl - MIN_BLOCK_SPACE

    left_counts, right_counts = zip(
        *((calculate_count(left_task, left_cursor),
           calculate_count(right_task, right_cursor(left_cursor)))
          for left_cursor in range(minl, maxl)))

    return sum(
        dleft * right
        for dleft, right in zip(__iderivative(left_counts), right_counts))


def calculate(task, length):
    """
    Calculates all combination of spans for specific task.

    Since combinations are lazy-calculated, the field may be already partially solved,
    so line is provided to avoid combinations that are eliminated.
    """
    if len(task) == 0:
        return []

    head, tail = task[0], task[1:]

    if not tail:
        return [[step] for step in range(length - head + 1)]

    move_space = calculate_moves(tail, length - head)

    head_steps = ((step, step + head + 1) for step in range(move_space))
    return [[hstep, *tsteps] for hstep, trim in head_steps
            for tsteps in calculate(tail, length - trim)]


def collapse(task, combinations, length):
    """
    Returns defined cells based on all combination
    Undefined cells marked as Cell.EMPTY (-1)
    """
    mask = np.zeros(length, np.int32)
    for steps in combinations:
        line = cline.array(task, steps, length)
        mask = np.add(mask, line)

    empty_or_filled, filled = mask > 0, mask == len(combinations)
    return Cell.EMPTY * empty_or_filled + (Cell.FILLED - Cell.EMPTY) * filled