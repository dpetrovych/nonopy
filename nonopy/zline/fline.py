from nonopy.cell import Cell
'''Operations over field line'''

def find_center_x(l):
    middle = len(l) // 2 - (len(l) - 1) % 2
    for left_i in range(middle, -1, -1):
        if l[left_i] == Cell.CROSSED:
            return left_i + 1
        if l[-1 - left_i] == Cell.CROSSED:
            return len(l) - left_i
    return None


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


def trim_x(line):
    trimmed_l_line, left_i = triml_x(line)
    trimmed_line, right_i = trimr_x(trimmed_l_line)
    return trimmed_line, left_i, right_i