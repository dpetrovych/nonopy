import os.path
import sys
from argparse import ArgumentParser

from nonopy import Parser, Solver
from nonopy.out import print_grid
from nonopy.log import PrintLog

parser = ArgumentParser(description='Solves nonogram file')
parser.add_argument('path', help='path to .non format file')
parser.add_argument('--verbose', '-v', action='count', default=0, help='shows actions')

args = parser.parse_args()

parser = Parser()
nonogram = None
with open(args.path, 'r') as f:
    nonogram = parser.parse(f.readlines())

log = PrintLog() if args.verbose else None
solver = Solver(nonogram.task, log=log)
grid = solver.solve(True)

print(print_grid(grid))
print(solver)