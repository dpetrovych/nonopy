from .parser import Parser
from .solver import Solver as SolverA
from .solverb import Solver as SolverB
from .solverc import Solver as SolverC

__solvers = {
    'A': SolverA,
    'B': SolverB,
    'C': SolverC,
}

def get_solver(key='A'):
    return __solvers[key]