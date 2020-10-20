import re

class Nonogram:
    def __init__(self, *, height, width, rows, columns, goal):
        if height <= 0:
            raise ValueError('height should be > 0')

        if width <= 0:
            raise ValueError('width should be > 0')

        if (rows_len := len(rows)) != height:
            raise ValueError(f'rows length {rows_len} shoule be equal {height}')

        if (columns_len := len(columns)) != width:
            raise ValueError(f'columns length {columns_len} shoule be equal {width}')
        
        goal_pattern = re.compile(f"([01]{{{width}}}\n){{{height}}}")

        if not goal_pattern.fullmatch(goal):
            raise ValueError(f'goal should be a string of {height} rows, [01]{{{width}}} characters each, end with an empty line')

        self.height = height
        self.width = width
        self.rows = rows
        self.columns = columns
        self.goal = goal
    
    def __repr__(self):
        return f'Goal:\n{self.goal}\nRows:\n{self.rows}\n\nColumns:\n\n{self.columns}'