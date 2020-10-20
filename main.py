import os.path
import sys

from nonopy import Parser

fname = sys.argv[1]
parser = Parser()
with open(fname, 'r') as f:
    nonogram = parser.parse(f.readlines())
    print(nonogram)
