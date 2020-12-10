from argparse import ArgumentParser, FileType
import os.path
import sys

from tabulate import tabulate

from nonopy import Parser, get_solver, clear_cache
from nonopy.format import format_grid, format_ms_time
from nonopy.log import create_logger_context
from nonopy.metrics import Metrics


def print_solvers_stats(solutions, filename=''):
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

    headers = [filename, *(solver_key for solver_key, _ in solutions)]
    table = zip(
        rows,
        *((
            status,
            *(format_ms_time(t)
              for t in metrics.list_values_sum('init.time', 'collapse.time')),
            metrics.get_values_sum('complexity'),
            *metrics.list_events_count(
                'init', 'collapse', 'sub_collapse.divide_by_crossed',
                'sub_collapse.divide_by_filled', 'sub_collapse.inplace'),
        ) for _, (_, status, metrics) in solutions))

    print(tabulate(table, headers=headers))


def print_line_stats(solutions, nonogram, sort_by):
    for solver_key, (_, _, metrics) in solutions:
        headers = [
            solver_key, 'task', 'complexity', '# collapse', 't collapse (ms)'
        ]
        floatfmt = (None, None, None, None, ".2f")

        def collapse_line_tuple(tasks, order):
            for i, task in enumerate(tasks):
                line_id = f'{order}{i}'
                yield [
                    line_id,
                    task,
                    metrics.get_values_sum(f'complexity.{line_id}'),
                    metrics.get_event_count(f'collapse.{line_id}'),
                    metrics.get_values_sum(f'collapse.time.{line_id}') /
                    1_000_000,
                ]

        table = [
            *collapse_line_tuple(nonogram.task.columns, 'c'),
            *collapse_line_tuple(nonogram.task.rows, 'r'),
        ]

        if sort_by != 0:
            sort_desc = sort_by < 0
            sort_by_index = (-sort_by if sort_desc else sort_by) - 1
            table = sorted(table,
                           key=lambda x: x[sort_by_index],
                           reverse=sort_desc)

        print()
        print(tabulate(table, headers=headers, floatfmt=floatfmt))


def main(args):
    nonogram = None
    with args.path as f:
        parser = Parser()
        nonogram = parser.parse(f.readlines())

    logger = create_logger_context(nonogram.task,
                                   interactive=args.interactive,
                                   verbose=args.verbose)

    def solve(Solver):
        metrics = Metrics()
        with logger as log:
            solver = Solver(metrics, log)
            grid = solver.solve(nonogram.task)
            status = 'solved' if grid is not None else 'unsolved'
            clear_cache()
            return grid, status, metrics

    solutions = [(k, solve(get_solver(k))) for k in args.solvers]

    if not args.nogrid:
        grid = solutions[0][1][0]
        print(format_grid(grid))

    print_solvers_stats(solutions, filename=f.name)

    if args.linestats is not None:
        print_line_stats(solutions, nonogram, args.linestats)


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
                        action='store_true',
                        help='shows actions log')

    parser.add_argument('--interactive',
                        '-i',
                        action='store_true',
                        help='shows grid while solving')

    parser.add_argument(
        '--nogrid',
        '-G',
        action='store_true',
        help='hides grid in final output (for comparing stats only)')

    parser.add_argument(
        '--linestats',
        metavar='SORTBY',
        nargs='?',
        const=0,
        type=int,
        help=
        'shows statistics per line sorted by column 1-based index (negative values for sorting in descending order)'
    )

    args = parser.parse_args()
    main(args)