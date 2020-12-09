from tabulate import tabulate

from nonopy.cell import Cell


def format_line(line, empty=' ', crossed='0', filled='1'):
    m = {Cell.FILLED: filled, Cell.CROSSED: crossed, Cell.EMPTY: empty}

    return f"|{''.join(map(m.get, line))}|"


def format_grid(grid, empty=' ', crossed=' ', filled='█', width=2):
    if grid is None:
        return

    table_body = '\n'.join(
        format_line(row,
                    empty=empty * width,
                    crossed=crossed * width,
                    filled=filled * width) for row in grid)
    table_dash = '─' * width * grid.shape[1]
    return f"┌{table_dash}┐\n{table_body}\n└{table_dash}┘"


def format_stats(solutions, filename=''):
    rows = [
        'status',
        't init',
        't solve',
        'complexity',
        '# init',
        '# collapse',
    ]

    headers = [filename, *(k for k, _ in solutions)]
    table = zip(
        rows,
        *((
            s,
            *(format_ns_time(t) for t in m.get_value_sum('init.time', 'collapse.time')),
            m.get_values('complexity')[0],
            *m.get_event_count('init', 'collapse'),
        ) for _, (_, s, m) in solutions))

    print(tabulate(table, headers=headers))

def format_ns_time(t_ns):
    """Formats time to millisecond float value

    Args:
        t (int): time in nanoseconds
    
    Returns:
        str
    """
    t_ms = t_ns / 1_000_000
    return f'{t_ms:.0f} ms'