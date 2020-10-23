import re

class Nonotask:
    def __init__(self, *, rows, columns):
        self.rows = rows
        self.columns = columns

    def __repr__(self):
        return f'Rows:\n{self.rows}\n\nColumns:\n\n{self.columns}'

    def get_height(self):
        return len(self.rows)
    
    def get_width(self):
        return len(self.columns)
    
    height = property(get_height)
    width = property(get_width)

class Nonogram:
    def __init__(self, task, goal):
        goal_pattern = re.compile(f"([01]{{{task.width}}}\n){{{task.height}}}")
        if not goal_pattern.fullmatch(goal):
            raise ValueError(f'goal should be a string of {task.height} rows, [01]{{{task.width}}} characters each, end with an empty line')

        self.task = task
        self.goal = goal
    
    def __repr__(self):
        return f'Goal:\n{self.goal}\n{repr(self.task)}'