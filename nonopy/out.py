def print_line(line, crossed=' ', filled='■'):
    return f"|{''.join(filled if c == 1 else crossed if c == 0 else ' ' for c in line)}|"

def print_grid(grid, crossed=' ', filled='■'):
    table_body = '\n'.join(print_line(row, crossed=crossed * 2, filled=filled * 2) for row in grid)
    table_dash = '──' * grid.shape[1]
    return f"┌{table_dash}┐\n{table_body}\n└{table_dash}┘"