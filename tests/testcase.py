from unittest import TestCase as UTestCase

class TestCase(UTestCase):
    def assertArrayEqual(self, first, second):
        self.assertEquals(len(first), len(second), msg=f"count missmatched")
        self.assertTrue((first == second).all(), msg=f"{first} != {second}")