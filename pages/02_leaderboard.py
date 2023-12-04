import streamlit as st
import random
import time
import pandas as pd
import numpy as np
import copy
from db_util import db_execute_query, db_select_query
from code_util import execute_code


def find_winner(board):
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] != 0) or (board[0][i] == board[1][i] == board[2][i] != 0):
            return True
    if (board[0][0] == board[1][1] == board[2][2] != 0) or (board[0][2] == board[1][1] == board[2][0] != 0):
        return True
    # now check for a tie
    if 0 in sum(board, []):
        return False
    return "Tie"

def print_board(board):
    """
        1   2   3
      +---+---+---+
    0 |   | X | X |
      +---+---+---+
    1 | X | O | X |
      +---+---+---+
    2 | O | O | O |
      +---+---+---+
    """
    symbol_map = {0: " ", 1: "X", 2: "O"}
    str_board = "\n##  0   1   2\n"
    for i in range(3):
        str_board += "  +---+---+---+\n"
        line = f"{i} |"
        for j in range(3):
            line += f" {symbol_map[board[i][j]]} |"
        str_board += line + "\n"
    str_board += "  +---+---+---+\n"
    # print(str_board)
    return str_board


def put_a_stone(board, x, y, stone):
    if board[x][y] == 0:
        board[x][y] = stone
        return board, True
    else:
        # print(f"Spot {x},{y} is already occupied. Try another spot.")
        return board, False


def exchange_order(org_board):
    board = copy.deepcopy(org_board)
    for row in board:
        for i in range(len(row)):
            if row[i] == 1:
                row[i] = 2
            elif row[i] == 2:
                row[i] = 1
    return board

# set global variable to save time and memory
STONE_INDEX = [(x, y) for x in range(3) for y in range(3)] 
def random_board(board):
    random_stone_num = random.randint(0, 9) # random stone number
    if random_stone_num != 0:
         for i in range(random_stone_num):
             random_stone = random.choice(STONE_INDEX) # (x, y)
             random_mark = random.choice([1, 2]) # 1 or 2
             board[random_stone[0]][random_stone[1]] = random_mark
             # if initialized winner, roll back 
             if find_winner(board):
                 board[random_stone[0]][random_stone[1]] = 0 
    return board

st.title(":trophy: TTT Leaderboard")

student_records = db_select_query("SELECT * FROM students")
random.shuffle(student_records) # to avoid the effect of game order
student_num = len(student_records)

if student_num < 2:
    st.warning("At least two students participated are required to start the tournament!")
else:  
    page_refresh = True
    ## header two columns
    cols = st.columns(2)
    with cols[0]:
        refresh = st.button("Refresh")
    with cols[1]:
        random_button = st.checkbox('Random Initialized Board') 
        
    if page_refresh or refresh or random_button:
        with st.spinner(text='In progress ...'):
            win_results = [[0 for i in range(student_num)] for j in range(student_num)] # n x n
            bar = st.progress(0)
            for i in range(student_num-1):
                # show progress
                player1 = list(student_records[i])
                for j in range(i+1, student_num):
                    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                    player2 = list(student_records[j])
                    print("### Round {}: {} (X) vs {} (O)".format(i, player1[0], player2[0]))
                    
                    # for version 2 
                    if random_button:
                        board = random_board(board)

                    print("**======> Start Playing <======**")
                    step = 1
                    while (True):
                        print(f"--------------- Step {step} ---------------")
                        step += 1 
                        # Execute the student 1 code of next_move() function to get their choice
                        play1_code = f"{player1[1]}\nboard = {copy.deepcopy(board)}\nprint(next_move(board))"   
                        try:   
                            player1_choice, _ = execute_code(play1_code) 
                            play1_x, play1_y = eval(player1_choice)
                        except:
                            print(f"{player1[0]}'s code made an Exception. {player2[0]} wins!")
                            print(print_board(board)) 
                            win_results[j][i] = 1
                            win_results[i][j] = -1
                            break
                        
                        board, valid_move = put_a_stone(board, play1_x, play1_y, 1)
                        if not valid_move:
                            print(f"{player1[0]}: {player1_choice}")
                            print(f"{player1[0]} made an invalid move due to spot is already occupied. {player2[0]} wins!")
                            print(print_board(board)) 
                            win_results[j][i] = 1
                            win_results[i][j] = -1
                            # print(win_results)
                            break

                        print(f"{player1[0]}: {player1_choice}")
                        print(print_board(board))

                        win_flag = find_winner(board)
                        if win_flag:
                            if "Tie" != win_flag:
                                result = f"The winner is {player1[0]}!"
                                win_results[i][j] = 1
                                win_results[j][i] = -1
                                # print(win_results)
                            else:
                                result = f"They are {win_flag}!"
                            print(result, "\n")
                            break

                        # ---------------------------------------------------------------------
                        # Execute the student 2 code of next_move() function to get their choice
                        play2_code = f"{player2[1]}\nboard = {exchange_order(copy.deepcopy(board))}\nprint(next_move(board))" 
                        try:
                            player2_choice, _ = execute_code(play2_code) 
                            play2_x, play2_y = eval(player2_choice)
                        except:
                            print(f"{player2[0]}'s code made an Exception. {player1[0]} wins!")
                            print(print_board(board)) 
                            win_results[i][j] = 1
                            win_results[j][i] = -1
                            break
                        
                        board, valid_move = put_a_stone(board, play2_x, play2_y, 2)
                        if not valid_move:
                            print(f"{player2[0]}: {player2_choice}")
                            print(f"{player2[0]} made an invalid move due to spot is already occupied. {player1[0]} wins!")
                            print(print_board(board)) 
                            win_results[i][j] = 1
                            win_results[j][i] = -1
                            # print(win_results)
                            break  

                        print(f"{player2[0]}: {player2_choice}")
                        print(print_board(board))

                        win_flag = find_winner(board)
                        if win_flag:
                            if "Tie" != win_flag:
                                result = f"The winner is {player2[0]}!"
                                win_results[j][i] = 1
                                win_results[i][j] = -1
                                # print(win_results)
                            else:
                                result = f"They are {win_flag}!"
                            print(result)
                            break

                bar.progress((i+1)*100//(student_num-1))
                time.sleep(0.1)
            # Update the database
            for k in range(student_num):
                win_num = win_results[k].count(1)
                lose_num = win_results[k].count(-1)
                student = student_records[k]
                db_execute_query("UPDATE students SET win = ?, lose = ? WHERE student_id = ?", (win_num, lose_num, student[0])) 
            st.success("Refresh successfully!") 
    
    # leadboard display
    student_records = db_select_query("SELECT * FROM students ORDER BY win DESC")
    table_data = []
    for record in student_records:
        table_data.append((record[0], record[2], record[3]))
    win_lose_result = pd.DataFrame(table_data, columns=("Student ID", "Win", "Lose"), index=[i+1 for i in range(student_num)])
    st.table(win_lose_result)