class RecursionPriority:
    def run_left_first(self, left, right):
        """Defines if left segment should be run recursively first

        Args:
            left (CollapseRun): left run segment
            right (CollapseRun): right run segment

        Returns:
            bool: if left segment should run first
        """
        return True


class TaskLengthPriority(RecursionPriority):
    def run_left_first(self, left, right):
        return len(left.task) <= len(right.task)