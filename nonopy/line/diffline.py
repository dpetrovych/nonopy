from nonopy.cell import Cell


def diff(field_line, collapse_line):
    """Generates array of Cell non-None in indexes where 2 lines are different"""
    if len(field_line) != len(collapse_line):
        raise Exception(
            f'Length mismatch: collapsed len {len(collapse_line)} != field line len {len(field_line)}'
        )

    def __diffiter(new_line, old_line):
        for new, old in zip(new_line, old_line):
            yield new if new != old else None

    return [*__diffiter(collapse_line, field_line)]


def reversed_diff(line_diff):
    """Generates diff line to reset EMPTY cell where previously defined (CROSSED OR FILLED) was set"""
    return [d if d is None else Cell.EMPTY for d in line_diff]
