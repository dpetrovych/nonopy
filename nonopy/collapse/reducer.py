import numpy as np

from nonopy.cell import Cell
from nonopy.collapse.result import CollapseResult


class BulkReducer:
    def reduce(self, results, length):
        '''Combine results from multiple divisions

        Args:
            combinations (Iterable[CollapsedResult|None]): iterable of all division results
            length (int): length of a line/section

        Returns:
            CollapseResult|None: a reduction result
        '''
        non_empty_results = [
            *filter(lambda result: result is not None, results)
        ]
        if len(non_empty_results) == 0:
            return None

        count = sum(l.count for l in non_empty_results)
        collapsed = np.array([l.line for l in non_empty_results], Cell.dtype)

        reduced = (Cell.FILLED if
                   (column == Cell.FILLED).all() else Cell.CROSSED if
                   (column == Cell.CROSSED).all() else Cell.EMPTY
                   for column in collapsed.T)

        return CollapseResult(np.fromiter(reduced, Cell.dtype, length), count)


class SlimReducer:
    def reduce(self, results, length):
        '''Combine results from multiple divisions as steam on each cycle to a single accumulated value

        Args:
            combinations (Iterable[CollapsedResult|None]): iterable of all division results
            length (int): length of a line/section

        Returns:
            CollapseResult|None: a reduction result
        '''
        accumulated = None
        count = 0
        for result in results:
            if result is None:
                continue

            count += result.count

            if accumulated is None:
                accumulated = result.line.copy()
                continue

            for i in range(length):
                if accumulated[i] != result.line[i]:
                    accumulated[i] = Cell.EMPTY

        return CollapseResult(accumulated, count) if accumulated is not None else None
