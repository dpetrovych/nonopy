from nonopy.cell import Cell
from nonopy.format import format_line
'''Operations over field line'''

def triml_x(line):
    left_i = 0
    while left_i < len(line) and line[left_i] == Cell.CROSSED:
        left_i += 1
    return line[left_i:], left_i

def trimr_x(line):
    right_i = 0
    while -right_i < len(line) and line[right_i - 1] == Cell.CROSSED:
        right_i -= 1

    return line[:right_i] if right_i < 0 else line[:], right_i


class FieldLine:
    def __init__(self, narray):
        self.narray = narray

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

    def __find_center(self, cell):
        '''Finding cell index next to a specific character (cell value) starting from the center'''
        middle = (len(self.narray) - 1) // 2
        for left_i in range(middle, -1, -1):
            if self.narray[left_i] == cell:
                return left_i + 1
            if self.narray[-1 - left_i] == cell:
                return len(self.narray) - left_i
        return None

    def find_center_x(self):
        return self.__find_center(Cell.CROSSED)

    def find_center_filled(self):
        return self.__find_center(Cell.FILLED)

    def trim_x(self):
        trimmed_l_line, left_i = triml_x(self.narray)
        trimmed_line, right_i = trimr_x(trimmed_l_line)
        return FieldLine(trimmed_line), left_i, right_i

    def to_array(self):
        return self.narray[:]