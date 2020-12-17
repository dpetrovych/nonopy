import numpy as np

from nonopy.cell import Cell
from nonopy.format import format_line
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
        '''Finding cell index next to a specific character (cell value) starting from the center'''
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
        if len(self.narray) != len(collapse_result.line):
            raise Exception(
                f'Length mismatch: collapsed len {len(collapse_result.line)} != field line len {len(self.narray)}'
            )

        def __diffiter(new_line, old_line):
            for new, old in zip(new_line, old_line):
                yield new if new != old else None

        return [*__diffiter(collapse_result.line, self.narray)]