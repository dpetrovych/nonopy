from tabulate import tabulate

from nonopy.cell import Cell

def format_line(line, empty=' ', crossed='0', filled='1'):
    m = {
        Cell.FILLED : filled,
        Cell.CROSSED : crossed,
        Cell.EMPTY : empty
    }

    return f"|{''.join(map(m.get, line))}|"


def format_grid(grid, empty=' ', crossed=' ', filled='█', width = 2):
    if grid is None:
        return

    table_body = '\n'.join(
        format_line(row, empty=empty * width, crossed=crossed * width, filled=filled * width)
        for row in grid)
    table_dash = '─' * width * grid.shape[1]
    return f"┌{table_dash}┐\n{table_body}\n└{table_dash}┘"


def format_stats(solutions, filename=''):
    rows = [
        'status', 'init', 'solve', 'complexity', 'cycles',
        'n_combinations', '-collapse', 'operations',
        '-collapse',
    ]

    headers = [filename, *(k for k, _ in solutions)]
    table = zip(
        rows,
        *((
            s,
            p.fvalue('init'),
            p.fvalue('solve'),
            m.complexity,
            m.cycles,
            None,
            *m.get_n_combinations('collapse'),
            None,
            *m.get_operations('collapse'),
        ) for _, (_, s, m, p) in solutions))

    print(tabulate(table, headers=headers))