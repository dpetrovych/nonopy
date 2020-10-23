class Collapse:
     def __init__(self, index, order, diff):
        self.index = index
        self.order = order
        self.diff = diff

class Log:
    def __init__(self):
        self.items = [] 

    def begin_collapse(self, order, index, *, count):
        pass

    def diff(self, order, index, *, diff):
        self.items.append(Collapse(index, order, diff))

    def filter(self, order, index, *, count_before, count_after):
        pass

class PrintLog(Log):
    def __init__(self):
        super()
    
    def begin_collapse(self, order, index, *, count):
        print('begin collapse', f'{order}{index}', 'count=', count)
        super().begin_collapse(order, index, count=count)
    
    def diff(self, order, index, *, diff):
        print('diff', f'{order}{index}', 'diff=', diff)
        super().diff(order, index, diff=diff)

    def filter(self, order, index, *, count_before, count_after):
        print('filter', f'{order}{index}', 'count=', f'{count_before} -> {count_after}')
        super().filter(order, index, count_before=count_before, count_after=count_after)



    