import os.path
import sys
from argparse import ArgumentParser, FileType

from nonopy import Parser, get_solver
from nonopy.out import print_grid, print_stats
from nonopy.log import PrintLog

parser = ArgumentParser(description='Solves nonogram file')

parser.add_argument('path',
                    help='path to .non format file',
                    type=FileType('r'))

parser.add_argument('--solvers',
                    '-s',
                    help='solvers to run (one-letter code for solver algorithm)',
                    type=str,
                    metavar='ABC',
                    default='A')

parser.add_argument('--verbose',
                    '-v',
                    action='count',
                    default=0,
                    help='shows actions')

args = parser.parse_args()

parser = Parser()
nonogram = None
with args.path as f:
    nonogram = parser.parse(f.readlines())

log = PrintLog() if args.verbose else None

def solve(Solver):
    solver = Solver(nonogram.task, log=log)
    grid = solver.solve()

    return grid, solver.status, solver.metrics, solver.perf


solutions = [(k, solve(get_solver(k))) for k in args.solvers]

if len(solutions) == 1:
    grid = solutions[0][1][0]
    print(print_grid(grid))

print_stats(solutions, filename=f.name)