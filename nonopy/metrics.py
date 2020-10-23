from collections import defaultdict

class Metrics:
    def __init__(self, combinations):
        self.complexity = sum(line.count for lines in combinations.values() for line in lines)
        self.line_instantiation = defaultdict(lambda: 0)

    def __repr__(self):
        return '\n'.join([f"complexity = {self.complexity}",
                          f"line instantiations:",
                          *(f'  {k.ljust(8)} = {v}'for k, v in self.line_instantiation.items()),
                          f'  total    = {sum(self.line_instantiation.values())}'])

    def add_line_instantiation(self, operation, count):
        self.line_instantiation[operation] += count
