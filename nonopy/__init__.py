from .parser import Parser
from .solver import Solver as SolverA
from .solverz import Solver as SolverZ

__solvers = {
    'A': SolverA,
    'Z': SolverZ,
}

def get_solver(key='A'):
    return __solvers[key]