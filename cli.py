from argparse import ArgumentParser, FileType
import os.path
import sys

from tabulate import tabulate

from nonopy import Parser, get_solver
from nonopy.format import format_grid, format_ns_time
from nonopy.log import create_logger_context


def format_stats(solutions, filename=''):
    rows = [
        'status',
        't init',
        't solve',
        'complexity',
        '# init',
        '# collapse',
        '- # calls: divide by crossed',
        '- # calls: divide by filled',
        '- # calls: inplace',
    ]

    headers = [filename, *(k for k, _ in solutions)]
    table = zip(
        rows,
        *((
            status,
            *(format_ns_time(t)
              for t in metrics.get_value_sum('init.time', 'collapse.time')),
            metrics.get_values('complexity')[0],
            *metrics.get_event_count(
                'init', 'collapse', 'sub_collapse.divide_by_crossed',
                'sub_collapse.divide_by_filled', 'sub_collapse.inplace'),
        ) for _, (_, status, metrics) in solutions))

    print(tabulate(table, headers=headers))

def main(args):
    nonogram = None
    with args.path as f:
        parser = Parser()
        nonogram = parser.parse(f.readlines())

    logger = create_logger_context(nonogram.task,
                                interactive=args.interactive,
                                verbose=args.verbose)


    def solve(Solver):
        with logger as log:
            solver = Solver(nonogram.task, log=log)
            grid = solver.solve()
            return grid, solver.status, solver.metrics


    solutions = [(k, solve(get_solver(k))) for k in args.solvers]

    if len(solutions) == 1:
        grid = solutions[0][1][0]
        print(format_grid(grid))

    format_stats(solutions, filename=f.name)


if __name__ == "__main__":
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
    main(args)