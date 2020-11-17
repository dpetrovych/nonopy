from .parser import Parser
from .solver import Solver as SolverA

__solvers = {
    'A': SolverA,
}


def get_solver(key='A'):
    return __solvers[key]