from itertools import takewhile

from nonopy.nonogram import Nonogram, Nonotask

class Parser():
    """Parses .non files, see examples in data/ folder"""

    def parse(self, lines):
        """Parses lines of a file in .non format to a structured information

        Args:
            lines (list[str]): a file represented as a list of lines

        Raises:
            ValueError: length of column or row array does not match width or height respectively

        Returns:
            Nonogram: object representing a puzzle
        """
        
        ilines = iter(lines)
        descriptor = {}
        while (line := next(ilines, None)):
            if line in {'rows\n', 'columns\n'}:
                descriptor[line.rstrip('\n')], line = self.__parse_multiline(ilines)
            
            if line is None:
                break

            if line == '\n':
                continue

            [key, value] = line.split(' ', 1)
            descriptor[key] = value.strip('"\n')

        self.__check_required_attributes(descriptor, ['height', 'width', 'rows', 'columns', 'goal'])

        height, width = int(descriptor['height']), int(descriptor['width'])
        rows, columns = descriptor['rows'], descriptor['columns']

        if (rows_len := len(rows)) != height:
            raise ValueError(f'rows length should be {height} (found {rows_len})')

        if (columns_len := len(columns)) != width:
            raise ValueError(f'columns length should be {width} (found {columns_len})')

        task = Nonotask(rows = rows, columns = columns)

        goal = descriptor['goal']
        if len(goal) != height * width:
            raise ValueError(f'goal length should be {height * width}')

        goal_formated = ''.join((goal[i * width: (i+1) * width] + '\n' for i in range(height)))
        return Nonogram(task, goal_formated)

    def __parse_multiline(self, iterator):
            """Parses a multiline value like as rows and columns tasks

            Args:
                iterator (iter): file lines iterator

            Returns:
                (list[list[int]], line): list of tasks and a current line
            """
            rows = []
            while (line := next(iterator, None)) is not None and line[0].isdigit():
                row_clues = line.rstrip('\n').split(',')
                rows.append([int(row_clue) for row_clue in row_clues])
            else: return rows, line

    def __check_required_attributes(self, descriptor, required_keys):
        for key in required_keys:
            if key not in descriptor:
                raise ValueError(f'{key} is required')