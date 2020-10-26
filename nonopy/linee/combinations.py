import numpy as np
from time import perf_counter

from nonopy.cell import Cell
import nonopy.line.cline as cline
"""Minimal space between 2 blocks"""
MIN_BLOCK_SPACE = 1


def calculate_moves(length, head, tail=None):
    """
    Calculates how many different positions can a head block have
    E.g.: if head == length and tail is [], there is only 1 position available - whole line lenght
    """
    if tail:
        return (length - head - sum(tail) - MIN_BLOCK_SPACE * len(tail) +
                MIN_BLOCK_SPACE)
    else:
        return length - head + MIN_BLOCK_SPACE


def calculate_hottask(task, length):
    """Calculates if task has block that produces filled cells on collapse on a clean line"""
    max_block = max(task)
    moves = calculate_moves(length, 0, task)
    return moves < max_block


def calculate_count(task, length):
    """
    Calculates how many combinations of spans (thus block positions) available for a specific task for a line length
    Helps to prioritize reduce operations before calculating actual spans
    """
    def rec_block_tigth_positions(t):
        head, tail = t[0], t[1:]
        if not tail:
            return [(head, head)]

        tail_pos = rec_block_tigth_positions(tail)
        last_pos = tail_pos[-1][1]
        tail_pos.append((head, last_pos + head + MIN_BLOCK_SPACE))
        return tail_pos

    block_pos_pairs = rec_block_tigth_positions(task)

    def rec_count(i, space_len):
        block, tail_pos = block_pos_pairs[i]
        move_space = space_len - tail_pos + 1 

        if i == 0:
            return move_space

        next_i = i - 1
        return sum(
            rec_count(next_i, space_len - block - step - MIN_BLOCK_SPACE)
            for step in range(0, move_space))

    return rec_count(len(block_pos_pairs) - 1, length)


def __match_line(cline, fline):
    return all(fcell == Cell.EMPTY or ccell == fcell
               for ccell, fcell in zip(cline, fline))


def calculate(task, line):
    """
    Calculates all combination of spans for specific task.

    Since combinations are lazy-calculated, the field may be already partially solved,
    so line is provided to avoid combinations that are eliminated.
    """
    head, tail = task[0], task[1:]
    move_space = calculate_moves(len(line), head, tail)

    if not tail:
        return [[step] for step in range(move_space)
                if __match_line(cline.iter_single(head, step, len(line)), line)
                ]

    head_steps = ((step, step + head + 1) for step in range(move_space))
    return [[hstep, *tsteps] for hstep, trim in head_steps
            if __match_line(cline.iter_single(head, hstep, trim), line[:trim])
            for tsteps in calculate(tail, line[trim:])]


def filter(task, combinations, line):
    """Returns combinations that matches current line"""
    return [
        steps for steps in combinations
        if __match_line(cline.iter(task, steps, len(line)), line)
    ]


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