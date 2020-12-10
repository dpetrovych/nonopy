# from nonopy.cell import Cell
# from nonopy.line.combinations import calculate_moves


# def should_run(task, field_line):
#     if len(task) > 0:
#         return calculate_moves(task, len(field_line)) >= 0
#     else:
#         return (field_line != Cell.FILLED).all()


# class PrioritizedRun:
#     def __init__(self, run):
#         self.run = run

#     def __call__(self, *, left, right):
#         if (not should_run(left.task, left.line)
#                 or not should_run(right.task, right.line)):
#             return None, None, 0

#         lresult, rresult = None, None
#         if len(left.task) <= len(right.task):
#             lresult = self.run(left.task, left.line)
#             if lresult is None:
#                 return None, None, 0

#             rresult = self.run(right.task, right.line)
#             if rresult is None:
#                 return None, None, 0
#         else:
#             rresult = self.run(right.task, right.line)
#             if rresult is None:
#                 return None, None, 0

#             lresult = self.run(left.task, left.line)
#             if lresult is None:
#                 return None, None, 0

#         return lresult, rresult, lresult.count * rresult.count
