from contextlib import nullcontext


def noop(**kwargs):
    pass


class Log:
    def init_line(self, order, index, *, task):
        return nullcontext(noop)

    def collapse(self, order, index, *, task, line, count):
        return nullcontext(noop)

    def checkpoint(self, order, index, *, cid, seed):
        return nullcontext(noop)
