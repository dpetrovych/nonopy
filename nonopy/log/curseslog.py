from contextlib import nullcontext
import curses
from time import perf_counter

from nonopy.log.log import Log
from nonopy.log.printlog import repr_index, end
from nonopy.format import format_line, format_grid
from nonopy.field import Field


class CursesLog(Log):
    LOG_RETENTION = 5
    GRID_PADDING = 2
    GRID_CHAR_WIDTH = 2

    def __init__(self, height, width):
        super().__init__()
        self.log = []
        self.height = height
        self.width = width
        self.field = Field(height, width)

        self.logpad_h = self.LOG_RETENTION
        self.fieldpad_h = self.height + self.GRID_PADDING
        self.window_h = self.logpad_h + self.fieldpad_h
        self.window_w = width * self.GRID_CHAR_WIDTH + self.GRID_PADDING

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.resize_term(self.window_h, self.window_w)
        self.logpad = curses.newpad(self.logpad_h + 1, self.window_w)
        self.fieldpad = curses.newpad(self.fieldpad_h + 1, self.window_w)
        return self

    def __exit__(self, *args):
        curses.echo()
        curses.endwin()

    def append_log(self, msg):
        self.log = self.log[-self.LOG_RETENTION + 1:]
        self.log.append(msg.ljust(self.window_w))

        for i, line in enumerate(self.log, 1):
            self.logpad.addstr(self.LOG_RETENTION - i, 0, line)

    def draw_field(self):
        grid_str = format_grid(self.field.grid, crossed='░')
        pritnable = ((i, line[:self.window_w])
                     for i, line in enumerate(grid_str.split('\n')))

        for i, line in pritnable:
            self.fieldpad.addstr(i, 0, line)

    def refresh(self):
        self.logpad.refresh(0, 0, 0, 0, self.logpad_h - 1, self.window_w - 1)
        self.fieldpad.refresh(0, 0, self.LOG_RETENTION, 0,
                              self.fieldpad_h + self.LOG_RETENTION - 1,
                              self.window_w - 1)
        self.stdscr.refresh()

    def init_line(self, order, index, *, task):
        start = perf_counter()
        self.append_log(
            f'line init start {repr_index(order, index)} task = {task}')
        self.refresh()

        def init_end(count=None):
            dt = perf_counter() - start
            self.append_log(
                f'{end()} {repr_index(order, index)} time = {dt:.3f}s  count = {count}'
            )
            self.refresh()

        return nullcontext(init_end)

    def collapse(self, order, index, *, task, line, count):
        format_field_line = format_line(line, crossed='x')
        self.append_log(
            f'collapse  start {repr_index(order, index)} line={format_field_line} count= {count} ')
        self.refresh()

        def collapse_end(diff):
            self.field.apply_diff(order, index, diff)
            self.append_log(
                f'{end()} {repr_index(order, index)} diff = {format_line(diff, crossed="x")}'
            )
            self.draw_field()
            self.refresh()

        return nullcontext(collapse_end)