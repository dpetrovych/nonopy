from .parser import Parser
from .solver import Solver as SolverA
from .solverb import Solver as SolverB
from .solverd import Solver as SolverD
from .solvere import Solver as SolverE

__solvers = {
    'A': SolverA,
    'B': SolverB,
    'D': SolverD,
    'E': SolverE,
}

def get_solver(key='D'):
    return __solvers[key]