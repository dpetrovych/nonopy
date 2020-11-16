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


def rec_block_tigth_positions(t):
    head, tail = t[0], t[1:]
    if not tail:
        return [(head, head)]

    tail_pos = rec_block_tigth_positions(tail)
    last_pos = tail_pos[-1][1]
    tail_pos.append((head, last_pos + head + MIN_BLOCK_SPACE))
    return tail_pos


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


def __match_line(cline, fline):
    return all(fcell == Cell.EMPTY or ccell == fcell
               for ccell, fcell in zip(cline, fline))


def calculate(task, line):
    """
    Calculates all combination of spans for specific task.

    Since combinations are lazy-calculated, the field may be already partially solved,
    so line is provided to avoid combinations that are eliminated.
    """
    if len(task) == 0:
        return []

    if (line == Cell.CROSSED).any():
        raise Exception(f'Should not contain CROSSED cell: {line}')

    block_pos_pairs = rec_block_tigth_positions(task)

    match_line = (__match_line if
                  (line != Cell.EMPTY).any() else lambda *args: True)

    def rec_calc(i, ln):
        head, tail_pos = block_pos_pairs[i]
        move_space = len(ln) - tail_pos + 1

        if i == 0:
            return [[step] for step in range(move_space)
                    if match_line(cline.iter_single(head, step, len(ln)), ln)]

        next_i = i - 1
        head_steps = ((step, step + head + 1) for step in range(move_space))
        return [[hstep, *tsteps] for hstep, trim in head_steps if match_line(
            cline.iter_single(head, hstep, trim), islice(ln, trim))
                for tsteps in rec_calc(next_i, ln[trim:])]

    return rec_calc(len(block_pos_pairs) - 1, line)


def collapse(task, combinations, length):
    """
    Returns defined cells based on all combination
    Undefined cells marked as Cell.EMPTY (-1)
    """
    mask = np.zeros(length, np.int32)
    for steps in combinations:
        line = cline.array(task, steps, length)
        mask = np.add(mask, line)

    # next optimisation assumes Cell.CROSSED == 0
    empty_or_filled, filled = mask > 0, mask == len(combinations)
    return Cell.EMPTY * empty_or_filled + (Cell.FILLED - Cell.EMPTY) * filled