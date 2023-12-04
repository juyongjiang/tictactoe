## Welcome to Tic-Tac-Toe Game
This app is made with [Streamlit](https://streamlit.io/). 
You can access our Tic-Tac-Toe Tournament platform at [https://tictactoe-john.streamlit.app](https://tictactoe-john.streamlit.app/home).

### Step 1: Upload Code

:computer: Please enter your student ID, password (initialized for the first time, after that, if you forget your password, please contact admin :cop: ), and complete \"next_move(board)\" strategy that returns x, y (the position of your next piece). In other words, your goal is to let \"Play 1 (You) :partying_face:\" win the game.
For example,

```python
# Input an board (3x3 list) as function argument,
# for example:
# board = [[0, 1, 0], [0, 0, 2], [0, 0, 0]], visualized as:
#  +---+---+---+
#  | 0 | 1 | 0 |
#  +---+---+---+
#  | 0 | 0 | 2 |
#  +---+---+---+
#  | 0 | 0 | 0 |
#  +---+---+---+
# 0: Empty
# 1: Piece of Play 1 (You)
# 2: Piece of Play 2 (Opponent)
# You need to complete the following function to return x, y, 
# which represents the position of next piece you place on the board.
# Don't place piece in the position that has been occupied, 
# otherwise, you will lost the game.

def next_move(board):
    import random
    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if board[x][y] == 0:
            return x, y
    return 0, 0
```
### Step 2: Play Game

**Tournament Results** 

Round 1: John vs Winner
======> Start Playing <======

--------------- Step 1 ---------------

John: (2, 0)
```python
##  0   1   2
  +---+---+---+
0 |   |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 | X |   |   |
  +---+---+---+
```

Winner: (0, 0)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 | X |   |   |
  +---+---+---+
--------------- Step 2 ---------------
```

John: (2, 1)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 | X | X |   |
  +---+---+---+
```

Winner: (2, 2)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 | X | X | O |
  +---+---+---+
```
--------------- Step 3 ---------------

John: (1, 0)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 | X |   |   |
  +---+---+---+
2 | X | X | O |
  +---+---+---+
```

Winner: (1, 1)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 | X | O |   |
  +---+---+---+
2 | X | X | O |
  +---+---+---+
```
The winner is Winner and continues to the next round!

**Tournament Standings** 
```python
Sung: 24
John: 12
```

### Step 3: Reset Database
After playing for a long time, if you want to clear the database, you can click this button.

## Lunch Project
```bash
touch .env
make 
make app
```