from .parser import Parser
from .solver import Solver as SolverA
from .solverx import Solver as SolverX
from .solvery import Solver as SolverY
from .solverz import Solver as SolverZ

__solvers = {
    'A': SolverA,
    'X': SolverX,
    'Y': SolverY,
    'Z': SolverZ,
}

def get_solver(key='A'):
    return __solvers[key]