import numpy as np
from itertools import islice, tee
from collections import defaultdict

from nonopy.cell import Cell, MIN_BLOCK_SPACE
from nonopy.format import format_line


def calculate_moves(task, length):
    return length - sum(task) - MIN_BLOCK_SPACE * len(task) + MIN_BLOCK_SPACE


def calculate_hottask(task, length):
    """Calculates if task has block that produces filled cells on collapse on a clean line"""
    max_block = max(task)
    return calculate_moves(task, length) < max_block


def __iderivative(iterator, start=0):
    prev = start
    for item in iterator:
        yield item - prev
        prev = item


__calc_n_cache = {}


def __calc_n(n, length):
    '''
    Calculate count of all combinations of n blocks of size 1 fit in length with spaces of size 1
    '''
    if n == 1:
        return length

    result = __calc_n_cache.get((n, length))
    if result:
        return result

    left_n = n // 2
    right_n = n - left_n
    minl, minr = 2 * left_n - 1, 2 * right_n - 1

    maxl = length - minr - 1
    maxr = length - minl - 1

    left_counts = (__calc_n(left_n, cursor) for cursor in range(minl, maxl + 1))
    right_counts = (__calc_n(right_n, cursor) for cursor in range(maxr, minr - 1, -1))

    result = __calc_n_cache[(n, length)] = sum(
        dleft * right
        for dleft, right in zip(__iderivative(left_counts), right_counts))

    return result


def calculate_count(task, length):
    """
    Calculates how many combinations of spans (thus block positions) available for a specific task for a line length
    Helps to prioritize reduce operations before calculating actual spans

    Uses divide & conquer strategy by dividing line in 2 and calculating respective counts in left and right parts.
    Than assembles results by multiplying.

    Also reduces all blocks in task to length of 1 and space to length of 1.
    """
    extra_block_space = (MIN_BLOCK_SPACE - 1) * (len(task) - 1)
    extra_block_len = sum(task) - len(task)
    return __calc_n(len(task), length - extra_block_space - extra_block_len)
