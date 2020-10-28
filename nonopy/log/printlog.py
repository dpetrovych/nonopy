from time import perf_counter

from nonopy.log.log import Log
from nonopy.format import format_line


def repr_index(order, index):
    return f'{order}{index}'.ljust(5)


def end():
    return 'end'.rjust(13).ljust(15)


class InitLinePerfContext():
    def __init__(self, order, index, *, task):
        self.order = order
        self.index = index
        self.task = task

    def __repr_index(self):
        return repr_index(self.order, self.index)

    def __enter__(self):
        self.start = perf_counter()
        print(f'line init start {self.__repr_index()} task = {self.task}')
        return self.log

    def log(self, count=None):
        if count:
            self.count = count

    def __exit__(self, type, value, tb):
        dt = perf_counter() - self.start
        print(
            f'{end()} {self.__repr_index()} time = {dt:.3f}s count = {self.count}'
        )


class PrintLog(Log):
    def __init__(self):
        super().__init__()

    def init_line(self, order, index, *, task):
        return InitLinePerfContext(order, index, task=task)

    def collapse_start(self, order, index, *, count):
        str_index = repr_index(order, index)
        print(f'collapse  start {str_index} count = {count}')
        return lambda diff: print(
            f'{end()} {str_index} diff = {format_line(diff, crossed="x")}')

    def filter_start(self, order, index, *, count):
        str_index = repr_index(order, index)
        print(f'filter    start {str_index} count = {count} -> ...')
        return lambda count_after: print(
            f'{end()} {str_index} count = {count} -> {count_after}')
