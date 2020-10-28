from contextlib import nullcontext


class Log:
    def init_line(self, order, index, *, task):
        return nullcontext(lambda **kvargs: None)

    def collapse_start(self, order, index, *, count):
        return lambda _: None

    def filter_start(self, order, index, *, count):
        return lambda _: None