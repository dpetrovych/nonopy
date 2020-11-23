# Nonopy

CLI and library for solving nonograms (aka griddlers, picross).
Supports puzzles with definite and deterministic solutions.

## CLI usage

```bash
python cli.py [-h] [--solvers ABC] [--verbose] [--interactive] path
```

### Positional arguments

|      |                          |
| ---- | ------------------------ |
| path | path to .non format file |

### Optional arguments

|                       |                                                       |
| --------------------- | ----------------------------------------------------- |
| --help, -h            | show this help message and exit                       |
| --solvers ABC, -s ABC | solvers to run (one-letter code for solver algorithm) |
| --verbose, -v         | shows actions log                                     |
| --interactive, -i     | shows grid while solving                              |

## Glossary

- _Field_ - 2d grid where a solved image is constructed
- _Line_ - column or row on the field
  - _Field line_ - representation of the current line state on the field
- _Block_ - consecutive filled cells in line (two blocks should be separated by 1+ crossed cells)
- _Task_ - numerical cues on top of the column (right to the row), represent block length
  - _Task line_ - abstraction that contains task and data/methods assosiated with row/column
  - _Hot task_ - task that has definite cells on empty line (can be solved in-place)
- _Collapse_ - operation of determining definite cell values based on the task and current line state

## Algorithm

### 0 RANGE lines
Calculates number of combinations of positionment of the blocks. Add lines with _hot tasks_ to the _hot heap_ - heap ordered desc by number of combinations.

### 1 POP the next line
Pop the line from the top of the _hot heap_ (thus with min combinations). 

### 2 COLLAPSE the line
To speed up collapse of combinations the solver uses some divide & conquere strategies.

#### DIVIDE_BY_CROSSED

#### DIVIDE_BY_FILLED

#### INPLACE

### 3 MARK lines hot

### 4 REPEAT until solved

Goto 1
