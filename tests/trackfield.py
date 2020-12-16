from nonopy.cell import Cell
from nonopy.field import Field
from nonopy.fieldtrack import FieldTrack
from nonopy.linelookup import LineLookup
from tests.testcase import TestCase


class TrackFieldShould(TestCase):
    def test_sets_field_and_combinations(self):
        combinations = LineLookup(rows=[2, 2], columns=[2, 2])
        field = Field(2, 2)
        track = FieldTrack(field, combinations)

        track.apply_diff('c', 0, [Cell.FILLED, Cell.CROSSED], -1)

        self.assertEqual(combinations['c', 0], 1)
        self.assertEqual(combinations['c', 1], 2)
        self.assertEqual(combinations['r', 0], 2)
        self.assertEqual(combinations['r', 1], 2)

        self.assertArrayEqual(field.grid[0], [1, -1])
        self.assertArrayEqual(field.grid[1], [0, -1])

    def test_rollback(self):
        combinations = LineLookup(rows=[2, 2], columns=[2, 2])
        field = Field(2, 2)
        track = FieldTrack(field, combinations)

        track.apply_diff('c', 0, [Cell.FILLED, Cell.CROSSED], -1)
        point = track.create_checkpoint()

        track.apply_diff('c', 1, [Cell.CROSSED, Cell.FILLED], -1)
        self.assertArrayEqual(field.grid[0], [1, 0])
        self.assertArrayEqual(field.grid[1], [0, 1])
        self.assertEqual(combinations['c', 1], 1)

        roll = track.rollback(point)
        
        self.assertListEqual(roll, [('c', 1, [0, 1], -1)])
        self.assertArrayEqual(field.grid[0], [1, -1])
        self.assertArrayEqual(field.grid[1], [0, -1])
        self.assertEqual(combinations['c', 1], 2)

