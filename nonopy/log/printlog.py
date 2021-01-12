from contextlib import nullcontext
from time import perf_counter

from nonopy.log.log import Log
from nonopy.format import format_line

LJ_ORDER = 15


def repr_index(order, index):
    return f'{order}{index}'.ljust(5)


def end():
    return 'end'.rjust(13).ljust(LJ_ORDER)


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

    def collapse(self, order, index, *, task, line, count):
        str_index = repr_index(order, index)
        format_field_line = format_line(line, crossed='x')
        start = perf_counter()
        print(
            f'collapse  start {str_index} line={format_field_line} cues={task.task} count= {count}'
        )

        def collapse_end(diff=None):
            format_diff = format_line(diff, crossed="x")
            dt = perf_counter() - start
            print(f'{end()} {str_index} diff={format_diff}')

        return nullcontext(collapse_end)

    def checkpoint(self, order, index, *, cid, seed):
        str_index = repr_index(order, index)
        print(f'{"checkpoint": <{LJ_ORDER}} {str_index} id={cid} seed={seed}')

        def rollback(backtrack=None):
            if backtrack is None:
                backtrack = []

            print(f'{"rollback": <{LJ_ORDER}} {str_index} seed={seed} n_backtrack={len(backtrack)}')
            for o, i, diff, count in backtrack:
                format_diff = format_line(diff, crossed="x")
                print(f'{"": <{LJ_ORDER}} {repr_index(o, i)} diff={format_diff} count_diff= {count}')

        return nullcontext(rollback)
