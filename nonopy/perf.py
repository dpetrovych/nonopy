from time import perf_counter

class PerfCounter:
    def __init__(self):
        self.start = {}
        self.stat = {}

    def __repr__(self): 
        return '\n'.join(f'{k}={v:8.3f}s'for k, v in self.stat.items())

    def solve_begin(self):
        self.start['solve'] = perf_counter()

    def solve_end(self):
        self.stat['solve'] =  perf_counter() - self.start['solve']