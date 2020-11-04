from unittest import TestCase as UTestCase

from nonopy.format import format_line

class TestCase(UTestCase):
    def assertArrayEqual(self, first, second):
        self.assertEquals(len(first), len(second), msg=f"count missmatched")
        self.assertTrue((first == second).all(), msg=f"\n{format_line(first)} !=\n{format_line(second)}")