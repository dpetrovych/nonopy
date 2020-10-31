import numpy as np

from nonopy.cell import Cell

def iter(task, steps, length):
    """Iterator that restors a complete line from task and steps"""
    cursor = 0
    for step, block in zip(steps, task):
        step += 0 if cursor == 0 else 1

        for _ in range(step):
            yield Cell.CROSSED
    
        for _ in range(block):
            yield Cell.FILLED

        cursor += step + block
    
    for _ in range(length - cursor):
        yield Cell.CROSSED

def iter_single(block, step, length):
    """Iterator that restors a complete line with a single block from its value and step before it"""
    for _ in range(step):
        yield Cell.CROSSED

    for _ in range(block):
        yield Cell.FILLED

    for _ in range(length - block - step):
        yield Cell.CROSSED

def array(task, steps, length):
    return np.fromiter(iter(task, steps, length), Cell.dtype)

def empty(length):
    """Generates an empty complete line of certain length"""
    return np.full(length, Cell.EMPTY, Cell.dtype)