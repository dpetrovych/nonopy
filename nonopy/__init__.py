from .parser import Parser
from .solver import Solver

from .collapse import Compute
from .collapse.priority import RecursionPriority, TaskLengthPriority

from .combinations import clear_cache

__solvers = {
    'A': lambda metrics, log: Solver(collapse=Compute(TaskLengthPriority(), None, metrics), metrics=metrics, log=log),
    'B': lambda metrics, log: Solver(collapse=Compute(RecursionPriority(), None, metrics), metrics=metrics, log=log),
}


def get_solver(key='A'):
    return __solvers[key]