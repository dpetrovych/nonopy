from itertools import takewhile

from nonopy.nonogram import Nonogram

class Parser():
    def parse(self, lines):
        """
        Parses string in .non format to a structured information
        """
        ilines = iter(lines)

        def parse_multiline(iterator):
            rows = []
            while (line := next(iterator, None)) is not None and line[0].isdigit():
                row_clues = line.rstrip('\n').split(',')
                rows.append([int(row_clue) for row_clue in row_clues])
            else: return rows, line
        
        descriptor = {}
        while (line := next(ilines, None)):
            if line in {'rows\n', 'columns\n'}:
                descriptor[line.rstrip('\n')], line = parse_multiline(ilines)
            
            if line == '\n':
                continue

            [key, value] = line.split(' ', 1)
            descriptor[key] = value.strip('"\n')

        height, width = int(descriptor['height']), int(descriptor['width'])
        rows, columns = descriptor['rows'], descriptor['columns']
        goal = descriptor['goal']
        goal_formated = ''.join((goal[i * width: (i+1) * width] + '\n' for i in range(height)))

        return Nonogram(height = height, width = width, rows = rows, columns = columns, goal = goal_formated)