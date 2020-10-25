from .parser import Parser
from .solver import Solver as SolverA
from .solverb import Solver as SolverB

__solvers = {
    'A': SolverA,
    'B': SolverB
}

def get_solver(key='A'):
    return __solvers[key]