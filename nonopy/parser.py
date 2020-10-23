from itertools import takewhile

from nonopy.nonogram import Nonogram, Nonotask

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

        if (rows_len := len(rows)) != height:
            raise ValueError(f'rows length {rows_len} shoule be {height}')

        if (columns_len := len(columns)) != width:
            raise ValueError(f'columns length {columns_len} shoule be {width}')

        task = Nonotask(rows = rows, columns = columns)

        goal = descriptor['goal']
        goal_formated = ''.join((goal[i * width: (i+1) * width] + '\n' for i in range(height)))

        return Nonogram(task, goal_formated)