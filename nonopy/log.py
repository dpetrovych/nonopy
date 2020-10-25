from nonopy.out import print_line

class Log:
    def collapse_start(self, order, index, *, count):
        return lambda _: None

    def filter_start(self, order, index, *, count):
        return lambda _: None

def repr_index(order, index):
    return f'{order}{index}'.ljust(5)

class PrintLog(Log):
    def __init__(self):
        super().__init__()
    
    def collapse_start(self, order, index, *, count):
        print('collapse start ', repr_index(order, index), 'count =', count)
        return lambda diff: print('         end   ', repr_index(order, index), 'diff =', print_line(diff, crossed = 'x'))

    def filter_start(self, order, index, *, count):
        print('filter   start ', repr_index(order, index), 'count =', f'{count} -> ...')
        return lambda count_after: print('         end   ', repr_index(order, index) , 'count =', f'{count} -> {count_after}')
