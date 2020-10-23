from unittest import TestCase

from nonopy.perf import PerfCounter

class PerfCounterShould(TestCase):
    def test_repr(self):
        counter = PerfCounter()
        counter.solve_begin()
        counter.solve_end()

        self.assertEquals(repr(counter), 'solve=   0.000s')