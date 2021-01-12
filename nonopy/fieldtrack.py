from nonopy.field import Field
from nonopy.line.diffline import reversed_diff
from nonopy.linelookup import LineLookup


class FieldTrack:
    def __init__(self, field: Field, combinations: LineLookup):
        self.field = field
        self.combinations = combinations
        self.log = []

    def apply_diff(self, order, index, line_diff, count_diff):
        """Set line diff to the field, count diff to combinations lookup and logs each action
        Args:
            order (str): order of line
            index (int): index of line
            line_diff (List[Cell]): field line difference
            count_diff ([type]): combinations count difference
        """
        self.log.append((order, index, line_diff, count_diff))
        self.field.apply_diff(order, index, line_diff)
        self.combinations[order, index] += count_diff

    def create_checkpoint(self):
        """Returns index of the next log item for rollback

        Returns:
            (int): rollback index
        """
        return len(self.log)

    def rollback(self, checkpoint):
        """Reverse actions of apply_diff until specified checkpoint index

        Args:
            checkpoint (int): rollback index

        Returns:
            List[(str, int, List[Cell], int)]: list of discarded log with following tuples: (order, index, line_diff, count_diff)
        """
        self.log, roll = self.log[:checkpoint], list(
            reversed(self.log[checkpoint:]))
        for order, index, line_diff, count_diff in roll:
            rev_line_diff = reversed_diff(line_diff)
            self.field.apply_diff(order, index, rev_line_diff)
            self.combinations[order, index] -= count_diff

        return roll
