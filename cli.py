from argparse import ArgumentParser, FileType
import curses
import os.path
import sys

from nonopy import Parser, get_solver
from nonopy.format import format_grid, format_stats
from nonopy.log import create_logger_context

parser = ArgumentParser(description='Solves nonogram file')

parser.add_argument('path',
                    help='path to .non format file',
                    type=FileType('r'))

parser.add_argument(
    '--solvers',
    '-s',
    help='solvers to run (one-letter code for solver algorithm)',
    type=str,
    metavar='ABC',
    default='A')

parser.add_argument('--verbose',
                    '-v',
                    action='count',
                    default=0,
                    help='shows actions log')

parser.add_argument('--interactive',
                    '-i',
                    action='count',
                    default=0,
                    help='shows grid while solving')

args = parser.parse_args()

parser = Parser()
nonogram = None
with args.path as f:
    nonogram = parser.parse(f.readlines())

logger = create_logger_context(nonogram.task,
                               interactive=args.interactive,
                               verbose=args.verbose)


def solve(Solver):
    with logger as log:
        solver = Solver(nonogram.task, log=log)
        grid = solver.solve()
        return grid, solver.status, solver.metrics, solver.perf


solutions = [(k, solve(get_solver(k))) for k in args.solvers]

if len(solutions) == 1:
    grid = solutions[0][1][0]
    print(format_grid(grid))

format_stats(solutions, filename=f.name)