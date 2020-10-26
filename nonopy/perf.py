from time import perf_counter
from collections import defaultdict


class TimeScope:
    def __init__(self, key, report):
        self.key = key
        self.report = report

    def __enter__(self):
        self.start = perf_counter()

    def __exit__(self, type, value, tb):
        span = perf_counter() - self.start
        self.report(self.key, span)


class PerfCounter:
    def __init__(self):
        self.stat = defaultdict(lambda: 0)

    def __repr__(self):
        return '\n'.join(f'{k.ljust(8)} = {v:8.3f}s'
                         for k, v in self.stat.items())

    def __report(self, key, value):
        self.stat[key] = value

    def init(self):
        return TimeScope('init', lambda key, value: self.__report(key, value))

    def solve(self):
        return TimeScope('solve', lambda key, value: self.__report(key, value))

    def fvalue(self, key):
        return f'{self.stat[key]:.3f}s'
