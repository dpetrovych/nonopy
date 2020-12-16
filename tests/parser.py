from nonopy.parser import Parser
from tests.testcase import TestCase


class ParserShould(TestCase):
    def test_empty_file(self):
        parser = Parser()

        with self.assertRaises(ValueError) as cm:
            parser.parse([])

        self.assertEqual(str(cm.exception), 'height is required')

    def test_min_valid_file(self):
        parser = Parser()
        content = '''
width 0
height 0
goal ""
rows

columns

'''
        nonogram = parser.parse(content.splitlines(True))

        self.assertEqual(nonogram.task.rows, [])
        self.assertEqual(nonogram.task.columns, [])
        self.assertEqual(nonogram.goal, '')

    def test_task_not_validated(self):
        parser = Parser()
        content = '''
width 2
height 2
goal "0000"
rows
1,1,1,1,1
100500

columns
1,2,3,4,5
0
'''
        nonogram = parser.parse(content.splitlines(True))

        self.assertListEqual(nonogram.task.rows, [[1, 1, 1, 1, 1], [100500]])
        self.assertListEqual(nonogram.task.columns, [[1, 2, 3, 4, 5], [0]])
        self.assertEqual(nonogram.goal, '00\n00\n')


    def test_invalid_n_rows(self):
        parser = Parser()
        content = '''
width 3
height 2
goal "101101"
rows
1,1

columns
2
0
2
'''
        with self.assertRaises(ValueError) as cm:
            parser.parse(content.splitlines(True))

        self.assertEqual(str(cm.exception), 'rows length should be 2 (found 1)')

    def test_invalid_n_columns(self):
        parser = Parser()
        content = '''
width 3
height 2
goal "101101"
rows
1,1
1,1

columns
2
0
2
0
'''
        with self.assertRaises(ValueError) as cm:
            parser.parse(content.splitlines(True))

        self.assertEqual(str(cm.exception), 'columns length should be 3 (found 4)')



    def test_goal_is_validated_for_length(self):
        parser = Parser()
        content = '''
width 2
height 2
goal "111111"
rows
2
2

columns
2
2
'''
        with self.assertRaises(ValueError) as cm:
            parser.parse(content.splitlines(True))

        self.assertEqual(str(cm.exception), 'goal length should be 4')

    
    def test_goal_has_invalid_chars(self):
        parser = Parser()
        content = '''
width 2
height 2
goal "abcd"
rows
2
2

columns
2
2
'''
        with self.assertRaises(ValueError) as cm:
            parser.parse(content.splitlines(True))

        self.assertEqual(str(cm.exception), 'goal should be a string of 2 rows, [01]{2} characters each, end with an empty line')
