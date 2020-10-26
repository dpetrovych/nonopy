from contextlib import nullcontext
from time import perf_counter

from nonopy.out import print_line

class Log:
    def init_line(self, order, index, *, task):
        return nullcontext(lambda **kvargs: None)

    def collapse_start(self, order, index, *, count):
        return lambda _: None

    def filter_start(self, order, index, *, count):
        return lambda _: None


def repr_index(order, index):
    return f'{order}{index}'.ljust(5)

def end():
    return '          end  '

class InitLinePerfContext():
    def __init__(self, order, index, *, task):
        self.order = order
        self.index = index
        self.task = task

    def __enter__(self):
        self.start = perf_counter()
        print('line init start', repr_index(self.order, self.index), 'task =', self.task)
        return self.log
    
    def log(self, count = None):
        if count:
            self.count = count

    def __exit__(self, type, value, tb):
        dt = perf_counter() - self.start
        print(end(), repr_index(self.order, self.index), 'time =', f'{dt:.3f}s', 'count =', self.count)


class PrintLog(Log):
    def __init__(self):
        super().__init__()

    def init_line(self, order, index, *, task):
        return InitLinePerfContext(order, index, task = task)

    def collapse_start(self, order, index, *, count):
        print('collapse  start', repr_index(order, index), 'count =', count)
        return lambda diff: print(end(), repr_index(order, index),
                                  'diff =', print_line(diff, crossed='x'))

    def filter_start(self, order, index, *, count):
        print('filter    start', repr_index(order, index), 'count =',
              f'{count} -> ...')
        return lambda count_after: print(end(),
                                         repr_index(order, index), 'count =',
                                         f'{count} -> {count_after}')
