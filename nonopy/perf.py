from time import perf_counter
from collections import defaultdict

class PerfCounter:
    def __init__(self):
        self.start = defaultdict(lambda: 0)
        self.stat = defaultdict(lambda: 0)

    def __repr__(self): 
        return '\n'.join(f'{k.rjust(8)} = {v:8.3f}s'for k, v in self.stat.items())

    def solve_begin(self):
        self.start['solve'] = perf_counter()

    def solve_end(self):
        self.stat['solve'] =  perf_counter() - self.start['solve']

    def fvalue(self, key):
        return f'{self.stat[key]:.3f}s'