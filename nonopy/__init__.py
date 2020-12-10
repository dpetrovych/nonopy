from .parser import Parser
from .solver import Solver

from .collapse import Compute
from .collapse.priority import RecursionPriority, TaskLengthPriority
from .collapse.reducer import SlimReducer, BulkReducer

from .combinations import clear_cache

__solvers = {
    'A':
    lambda metrics, log: Solver(collapse=Compute(TaskLengthPriority(),
                                                 SlimReducer(), metrics),
                                metrics=metrics,
                                log=log),
    'B':
    lambda metrics, log: Solver(collapse=Compute(RecursionPriority(), SlimReducer(),
                                                 metrics),
                                metrics=metrics,
                                log=log),
    
    'C':
    lambda metrics, log: Solver(collapse=Compute(TaskLengthPriority(),
                                                 BulkReducer(), metrics),
                                metrics=metrics,
                                log=log),
}


def get_solver(key='A'):
    return __solvers[key]