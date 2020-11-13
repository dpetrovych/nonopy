from .parser import Parser
from .solver import Solver as SolverA
from .solvery import Solver as SolverY
from .solverz import Solver as SolverZ

__solvers = {
    'A': SolverA,
    'Y': SolverY,
    'Z': SolverZ,
}

def get_solver(key='A'):
    return __solvers[key]