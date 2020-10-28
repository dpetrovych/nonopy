from contextlib import nullcontext

from .log import Log
from .printlog import PrintLog
from .curseslog import CursesLog

def create_logger_context(task, interactive = 0, verbose = 0):
    def create_curseslog():
        return CursesLog(task.height, task.width) if interactive else None

    def create_printlog():
        return nullcontext(PrintLog() if verbose else None)

    return create_curseslog() or create_printlog()