from collections import defaultdict

class Metrics:
    def __init__(self):
        self.complexity = 0
        self.operations = defaultdict(lambda: 0)
        self.cycles = 0

    def __repr__(self):
        return '\n'.join([f'complexity = {self.complexity}',
                          'operations:',
                          *(f'  {k.ljust(8)} = {v}'for k, v in self.operations.items()),
                          f'cycles = {self.cycles}'])

    def set_comlexity(self, combinations):
        self.complexity = sum(line.count for lines in combinations.values() for line in lines)

    def add_operation(self, operation):
        self.operations[operation] += 1

    def inc_cycle(self):
        self.cycles += 1
    
    def get_operations(self, *keys):
        return [self.operations[k] for k in keys]