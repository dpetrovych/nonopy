from contextlib import nullcontext


class Log:
    def init_line(self, order, index, *, task):
        return nullcontext(lambda **kvargs: None)

    def collapse(self, order, index, *, task, line):
        return nullcontext(lambda **kvargs: None)