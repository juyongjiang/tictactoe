code = """
# check whether the board has winner
def check_win(board):
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] != 0) or (board[0][i] == board[1][i] == board[2][i] != 0):
            return True
    if (board[0][0] == board[1][1] == board[2][2] != 0) or (board[0][2] == board[1][1] == board[2][0] != 0):
        return True
    return False


def next_move(board):
    board_flat = sum(board, [])
    non_zero = 9 - board_flat.count(0)
    if non_zero % 2 == 0:
        player = 1
        opposite = 2
    else: 
        player = 2
        opposite = 1

    # Check if we can win in the next move
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = player  # Temporarily make a move
                if check_win(board):  # Assuming there's a function to check winning
                    return i, j  # Return winning move
                else:
                    board[i][j] = 0  # Revert the move if it's not winning

    # Check if the opponent can win in the next move and block them
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = opposite  # Temporarily make a move for the opponent
                if check_win(board):  # Assuming there's a function to check winning
                    return i, j  # Return blocking move
                else:
                    board[i][j] = 0  # Revert the move if it's not blocking

    # If no immediate win or loss, just make the first available move
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                # further check the next step
                board[i][j] = player
                for k in range(3):
                    row = [board[k][0], board[k][1], board[k][2]]
                    if row.count(player) == 2 and row.count(0) == 1:
                        board[i][j] = 0
                        return i, j

                    column = [board[0][k], board[1][k], board[2][k]]
                    if column.count(player) == 2 and column.count(0) == 1:
                        board[i][j] = 0
                        return i, j

                diag = [board[0][0], board[1][1], board[2][2]]
                if diag.count(player) == 2 and diag.count(0) == 1:
                    board[i][j] = 0
                    return i, j

                reverse_diag = [board[0][2], board[1][1], board[2][0]]
                if reverse_diag.count(player) == 2 and reverse_diag.count(0) == 1:
                    board[i][j] = 0
                    return i, j
                board[i][j] = 0
                return i, j

    return 0, 0  # Return default move if no other move is found

board = [[1, 1, 2], [2, 2, 1], [1, 0, 0]]
result = next_move(board)
"""  

debug = """
def next_move(board):
    return 
board = [[1, 1, 2], [2, 2, 1], [1, 0, 0]]
result = next_move(board)
"""
# exec(debug)
# print(result is None)
def a(b):
    b.append(1)
    
    return b
b = [1,2,3]
c = a(b)
print(b)