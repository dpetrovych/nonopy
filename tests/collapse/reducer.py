from nonopy.collapse.reducer import BulkReducer, SlimReducer
from nonopy.collapse.result import CollapseResult
from tests.testcase import TestCase
from tests.utils import stoline


class BulkReducerShould(TestCase):
    def test_none_results(self):
        reducer = BulkReducer()

        result = reducer.reduce([None, None], 10)

        self.assertIsNone(result)

    def test_2_results(self):
        reducer = BulkReducer()

        result = reducer.reduce(
            [CollapseResult(stoline('|0011100|'), 1), None], 7)

        self.assertArrayEqual(result.line, stoline('|0011100|'))
        self.assertEqual(result.count, 1)

    def test_5_results(self):
        reducer = BulkReducer()

        result = reducer.reduce([
            CollapseResult(stoline('|001110 |'), 2),
            None,
            CollapseResult(stoline('|  00111|'), 5),
            None,
            CollapseResult(stoline('|   111 |'), 7)
        ], 7)

        self.assertArrayEqual(result.line, stoline('|    1  |'))
        self.assertEqual(result.count, 14)


class SlimReducerShould(TestCase):
    def test_none_results(self):
        reducer = SlimReducer()

        result = reducer.reduce([None, None], 10)

        self.assertIsNone(result)

    def test_2_results(self):
        reducer = SlimReducer()

        result = reducer.reduce(
            [CollapseResult(stoline('|0011100|'), 1), None], 7)

        self.assertArrayEqual(result.line, stoline('|0011100|'))
        self.assertEqual(result.count, 1)

    def test_5_results(self):
        reducer = SlimReducer()

        result = reducer.reduce([
            CollapseResult(stoline('|001110 |'), 2),
            None,
            CollapseResult(stoline('|  00111|'), 5),
            None,
            CollapseResult(stoline('|   111 |'), 7)
        ], 7)

        self.assertArrayEqual(result.line, stoline('|    1  |'))
        self.assertEqual(result.count, 14)