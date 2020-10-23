import numpy as np

from nonopy.cell import Cell
import nonopy.line.cline as cline

def __calc_moves(length, head, tail = None):
    """
    Calculates how many different positions can a head block have
    E.g.: if head == length and tail is [], there is only 1 position available - whole line lenght
    """
    return  length - head - sum(tail) - len(tail) + 1 if tail else length - head + 1

def calculate_count(task, length):
    """
    Calculates how many combinations of spans (thus block positions) available for a specific task for a line length
    Helps to prioritize reduce operations before calculating actual spans
    """
    head, tail = task[0], task[1:]
    move_space = __calc_moves(length, head, tail)
    
    if not tail:
        return move_space
    
    return sum(
        calculate_count(tail, length - head - step - 1) 
        for step in range(0, move_space))

def __match_line(cline, fline):
        return all(fcell == Cell.EMPTY or ccell == fcell for ccell, fcell in zip(cline, fline))

def calculate(task, line):
    """
    Calculates all combination of spans for specific task.

    Since combinations are lazy-calculated, the field may be already partially solved,
    so line is provided to avoid combinations that are eliminated.
    """
    head, tail = task[0], task[1:]
    move_space = __calc_moves(len(line), head, tail)

    if not tail:
        return [[step] 
            for step in range(move_space) 
            if __match_line(cline.iter_single(head, step, len(line)), line)]
    
    head_steps = ((step, step + head + 1) for step in range(move_space))
    return [[hstep, *tsteps] 
        for hstep, trim in head_steps
        if __match_line(cline.iter_single(head, hstep, trim), line[:trim])
        for tsteps in calculate(tail, line[trim:])]

def filter(task, combinations, line):
    """Returns combinations that matches current line"""
    return [steps for steps in combinations if __match_line(cline.iter(task, steps, len(line)), line)]

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