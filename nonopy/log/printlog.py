from contextlib import nullcontext
from time import perf_counter

from nonopy.log.log import Log
from nonopy.format import format_line


def repr_index(order, index):
    return f'{order}{index}'.ljust(5)


def end():
    return 'end'.rjust(13).ljust(15)


class PrintLog(Log):
    def __init__(self):
        super().__init__()

    def init_line(self, order, index, *, task):
        str_index = repr_index(order, index)
        start = perf_counter()
        print(f'line init start {str_index} task = {task}')

        def init_line_end(count=None):
            dt = perf_counter() - start
            print(f'{end()} {str_index} time = {dt:.3f}s count = {count}')

        return nullcontext(init_line_end)

    def collapse(self, order, index, *, task, line):
        str_index = repr_index(order, index)
        format_field_line = format_line(line, crossed='x')
        start = perf_counter()
        print(
            f'collapse  start {str_index} line={format_field_line} cues={task.task} count= {task.count}'
        )

        def collapse_end(diff=None):
            format_diff = format_line(diff, crossed="x")
            dt = perf_counter() - start
            print(f'{end()} {str_index} diff={format_diff}')

        return nullcontext(collapse_end)
