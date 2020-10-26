from unittest import TestCase

from nonopy.perf import PerfCounter

class PerfCounterShould(TestCase):
    def test_repr(self):
        counter = PerfCounter()
        with counter.solve():
            pass

        self.assertEquals(counter.fvalue('solve'), '0.000s')