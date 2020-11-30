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

## Legend
```
r10 - row with an index 10
c4 - column with an index 4
| - line boundary
· - empty cell
x - crossed cell
1 - filled cell
```

## Algorithm

### 0 RANGE lines
Calculates number of combinations of positionment of the blocks. Add lines with _hot tasks_ to the _hot heap_ - heap ordered desc by number of combinations.

### 1 POP the next line
Pop the line from the top of the _hot heap_ (thus with min combinations). 

### 2 COLLAPSE the line
To speed up collapse of combinations the solver uses some divide & conquere strategies.

#### DIVIDE_BY_CROSSED
If a line has already crossed boxes, it can solve 2 halfs of a line as separate lines.

```
line: |···xx···|
task: [2, 1, 1]
---
left: |···|     right: |···|
task: []         task: [2, 1, 1]
rslt: |xxxx|     rslt: None     -- Eliminated

left: |···|     right: |···|
task: [2]        task: [1, 1]
rslt: |·1·|      rslt: |1x1|    -> |·1·xx1x1|

left: |····|    right: |···|
task: [2, 1]     task: [1]
rslt: |11x1|     rslt: None   -- Eliminated

left: |····|    right: |···|
task: [2, 1, 1]  task: [1]
rslt: None       rslt: None     -- Eliminated
---
result: |·1·xx1x1|
```

#### DIVIDE_BY_FILLED
If a line has already filled boxes, it can fit one of the block on to the filled one and solve 2 parts with remaining blocks.
```
line: |··1····|
task: [2, 2]
---
Fit block 0 at index 1: |x11x···|
left: ||        right: |···|
task: []         task: [2]
rslt: ||         rslt: | 1 |    -> |x11x 1 |

Fit block 0 at index 2: |·x11x··|
left: |·|       right: |··|
task: []         task: [2]
rslt: |x|        rslt: |11|     -> |xx11x11|

Fit block 1 at index 1: |x11x···|
left: ||        right: |···|
task: [2]        task: []
rslt: None       rslt: |xxx|    -- Eliminated

Fit block 1 at index 2: |·x11x··|
left: |·|       right: |··|
task: [2]        task: []
rslt: None       rslt: |xx|     -- Eliminated

---
result: |x·1··1·|
```

#### INPLACE
INPLACE runs when all line cells are empty. In the logic of the move all blocks tightly to the left boudary, then to the right and mark the intersection of the same blocks.

This technick is also known as Simple Blocks. [(wiki)](https://en.wikipedia.org/wiki/Nonogram#Simple_boxes)

```
task: [3, 2]
line: |·······|
---
lshift: |111·11·|
rshift: |·111·11|
---
result: |·11··1·|
```

### 3 DIFF result with the line
Hightlight cells where new solution emerged from collapse operation.

Example (from [DIVIDE_BY_CROSSED](#DIVIDE_BY_CROSSED)):
```
line:   |···xx···|
result: |·1·xx1x1|
---
diff:   |·1···1x1|
```

### 4 MARK lines hot
For each highlighted diff cell mark an opposite direction (column if diff line is a row and vice versa) as hot and put to a __hot heap_.

Example:
```
diff r2: |·1···1x1|
marked hot: c1, c5, c6, c7
```

### 5 REPEAT until solved
[Goto 1](#1%20POP%20the%20next%20line)
