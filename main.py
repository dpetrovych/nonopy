import os.path
import sys

from nonopy import Parser, Solver

fname = sys.argv[1]
parser = Parser()

nonogram = None
with open(fname, 'r') as f:
    nonogram = parser.parse(f.readlines())

solver = Solver(nonogram.task)
print(solver)