import numpy as np

from nonopy.format import format_line
from nonopy.line.diffline import diff

'''Operations over field line'''


class FieldLine:
    def __init__(self, narray):
        self.narray = (narray
                       if isinstance(narray, np.ndarray) else np.array(narray))

    def __repr__(self):
        return format_line(self.narray)

    def __len__(self):
        return len(self.narray)

    def __getitem__(self, subscript):
        result = self.narray.__getitem__(subscript)
        if isinstance(subscript, slice):
            return FieldLine(result)
        else:
            return result

    def __eq__(self, other):
        if isinstance(other, FieldLine):
            return self.narray == other.narray
        else:
            return self.narray == other

    def __ne__(self, other):
        if isinstance(other, FieldLine):
            return self.narray != other.narray
        else:
            return self.narray != other

    def copy_with(self, index, cell):
        copy = self.narray.copy()
        copy[index] = cell
        copy.setflags(write=0)
        return FieldLine(copy)

    def find_center_cell(self, cell):
        """Finding cell index next to a specific character (cell value) starting from the center"""
        middle = (len(self.narray) - 1) // 2
        for left_i in range(middle, -1, -1):
            if self.narray[left_i] == cell:
                return left_i
            if self.narray[-1 - left_i] == cell:
                return len(self.narray) - left_i - 1
        return None

    def find_center_block(self, cell):
        f_start = self.find_center_cell(cell)
        if f_start is None:
            return f_start, None

        f_end = f_start + 1
        while f_start > 0 and self.narray[f_start - 1] == cell:
            f_start -= 1

        while f_end < len(self.narray) and self.narray[f_end] == cell:
            f_end += 1

        return f_start, f_end

    def diff(self, collapse_result):
        return diff(self.narray, collapse_result.line)
