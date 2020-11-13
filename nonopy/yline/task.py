from typing import List

from nonopy.cell import MIN_BLOCK_SPACE

Task = List[int]

def find_weight_center(task: Task):
    il, ir = 0, -1
    suml, sumr = -MIN_BLOCK_SPACE, -MIN_BLOCK_SPACE
    while il - ir <= len(task):
        if suml <= sumr:
            suml += task[il] + MIN_BLOCK_SPACE
            il += 1
        else:
            sumr += task[ir] + MIN_BLOCK_SPACE
            ir -= 1
    return il, (suml, sumr)