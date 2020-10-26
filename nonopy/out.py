from tabulate import tabulate


def print_line(line, crossed='0', filled='1'):
    return f"|{''.join(filled if c == 1 else crossed if c == 0 else ' ' for c in line)}|"


def print_grid(grid, crossed=' ', filled='■'):
    if grid is None:
        return

    table_body = '\n'.join(
        print_line(row, crossed=crossed * 2, filled=filled * 2)
        for row in grid)
    table_dash = '──' * grid.shape[1]
    return f"┌{table_dash}┐\n{table_body}\n└{table_dash}┘"


def print_stats(solutions, filename=''):
    rows = [
        'status', 'init', 'solve', 'complexity', 'cycles',
        'line_instantiations', '-collapse', '-filter', '-sum', 'operations',
        '-collapse', '-filter'
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
            *m.get_line_instantiation('collapse', 'filter', 'sum'),
            None,
            *m.get_operations('collapse', 'filter'),
        ) for _, (_, s, m, p) in solutions))

    print(tabulate(table, headers=headers))