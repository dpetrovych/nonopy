import numpy as np
from itertools import islice, tee

from nonopy.cell import Cell, MIN_BLOCK_SPACE
from nonopy.format import format_line
from nonopy.line.task import find_weight_center


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