from nonopy.cell import Cell


def format_line(line, empty=' ', crossed='0', filled='1'):
    """Formats a line for console output

    Args:
        line (list[int]): list (or any iterative object) representing values of a specific line
        empty (str, optional): character for an empty cell. Defaults to ' '.
        crossed (str, optional): character for a croseed cell. Defaults to '0'.
        filled (str, optional): character for a filled cell. Defaults to '1'.

    Returns:
        str: formatted line
    """
    m = {Cell.FILLED: filled, Cell.CROSSED: crossed, Cell.EMPTY: empty}

    return f"|{''.join(map(m.get, line))}|"


def format_grid(grid, empty=' ', crossed=' ', filled='█', width=2):
    """Formats a grid for console output

    Args:
        grid (list[list[int]]): a puzzle grid
        empty (str, optional): character for an empty cell. Defaults to ' '.
        crossed (str, optional): character for a croseed cell. Defaults to ' '.
        filled (str, optional): character for a filled cell. Defaults to '█'.
        width (int, optional): number of characters per cell. Defaults to 2.

    Returns:
        str: formatted grid
    """
    if grid is None:
        return

    table_body = '\n'.join(
        format_line(row,
                    empty=empty * width,
                    crossed=crossed * width,
                    filled=filled * width) for row in grid)
    table_dash = '─' * width * grid.shape[1]
    return f"┌{table_dash}┐\n{table_body}\n└{table_dash}┘"


def format_ns_time(t_ns):
    """Formats time to millisecond float value

    Args:
        t (int): time in nanoseconds
    
    Returns:
        str
    """
    t_ms = t_ns / 1_000_000
    return f'{t_ms:.0f} ms'