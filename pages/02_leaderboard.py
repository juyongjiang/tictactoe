import streamlit as st
import random
import time
import pandas as pd
import numpy as np
import copy
from db_util import db_execute_query, db_select_query
from code_util import execute_code

ADMIN = ['John', 'Sung', 'Jack']


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
        return True
    else:
        # print(f"Spot {x},{y} is already occupied. Try another spot.")
        return False


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
# random.shuffle(student_records) # to avoid the effect of game order
student_num = len(student_records)

cols = st.columns(2)
with cols[0]:
    student_id = st.text_input("Admin ID:", key="student_id")
with cols[1]:
    passcode = st.text_input("Password:", type="password", key="password")

if student_num < 2:
    st.warning("At least two students participated are required to start the tournament!")
else:  
    # page_refresh = True
    ## header two columns
    # cols = st.columns(2)
    # with cols[0]:
    refresh = st.button("Admin Refresh")
        
    # with cols[1]:
    #     random_button = st.checkbox('Random Initialized Board') 
    if refresh: # or random_button:
        if not student_id:
            st.error("Student ID cannot be empty.")
            st.stop()
        if not passcode:
            st.error("Password cannot be empty.")
            st.stop() 
        if student_id not in ADMIN:
            st.error("You are not authorized to refresh the tournament!")
            st.stop()
        else:
            st.info("Welcome Admin!")
        
        for record in student_records:
            db_execute_query("UPDATE students SET win = ?, lose = ?, tie = ? WHERE student_id = ?", (0, 0, 0, record[0]))  
        student_records = db_select_query("SELECT * FROM students") 
        
        student_data = db_select_query('SELECT * FROM students WHERE student_id=?', (student_id,)) # return a list
        if len(student_data)!=0 and student_id in ADMIN:  
            if passcode == student_data[0][4]:
                with st.spinner(text='In progress ...'):
                    # win_results = [[0 for i in range(student_num)] for j in range(student_num)] # n x n
                    # win_results = [[0] * student_num] * student_num # n x n
                    bar = st.progress(0)
                    for i, player_1 in enumerate(student_records):
                        # show progress
                        player1 = list(player_1)
                        for j, player_2 in enumerate(student_records):
                            if player1[0] == player_2[0]: # name is the same
                                continue
                            board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                            player2 = list(player_2)
                            
                            print("### Round {}-{}: {} (X) vs {} (O)".format(i+1, j+1, player1[0], player2[0]))
                            # for version 2 
                            # if random_button:
                            #     board = random_board(board)
                            print("**======> Start Playing <======**")
                            step = 1
                            while (True):
                                print(f"---------------{i}-{j} Step {step} ---------------")
                                step += 1 
                                # Execute the student 1 code of next_move() function to get their choice
                                play1_code = f"""{player1[1]}\nboard_copy = {copy.deepcopy(board)}\nplayer_1_move = next_move(board_copy)"""  
                                exec(play1_code) 
                                if player_1_move is None:
                                    print(f"{player1[0]}'s code return None! {player2[0]} wins!")
                                    print(print_board(board)) 
                                    player1[3] += 1
                                    break
                                else: # is not None:
                                    play1_x, play1_y = player_1_move
                                    valid_move = put_a_stone(board, play1_x, play1_y, 1)
                                if not valid_move:
                                    print(f"{player1[0]} => {player_1_move}")
                                    print(print_board(board)) 
                                    print(f"{player1[0]} made an invalid move due to spot is already occupied. {player2[0]} wins!")
                                    player1[3] += 1
                                    break
                                else:
                                    print(f"{player1[0]} => {player_1_move}")
                                    print(print_board(board))

                                win_flag = find_winner(board)
                                if win_flag:
                                    if "Tie" != win_flag:
                                        result = f"The winner is {player1[0]}!"
                                        player1[2] += 1
                                    else:
                                        result = f"They are {win_flag}!"
                                        player1[5] += 1
                                    print(result, "\n")
                                    break

                                # ---------------------------------------------------------------------
                                # Execute the student 2 code of next_move() function to get their choice
                                play2_code = f"""{player2[1]}\nboard_copy = {copy.deepcopy(board)}\nplayer_2_move = next_move(board_copy)"""
                                exec(play2_code)
                                if player_2_move is None:
                                    print(f"{player2[0]}'s code return None! {player1[0]} wins!")
                                    print(print_board(board)) 
                                    player1[2] += 1
                                    # win_results[i][j] = 1
                                    # win_results[j][i] = -1
                                    break
                                else: # is not None:
                                    play2_x, play2_y = player_2_move
                                    valid_move = put_a_stone(board, play2_x, play2_y, 2)
                                if not valid_move:
                                    print(f"{player2[0]} => {player_2_move}")
                                    print(print_board(board)) 
                                    print(f"{player2[0]} made an invalid move due to spot is already occupied. {player1[0]} wins!")
                                    player1[2] += 1
                                    # win_results[i][j] = 1
                                    # win_results[j][i] = -1
                                    # print(win_results)
                                    break  
                                else:
                                    print(f"{player2[0]} => {player_2_move}")
                                    print(print_board(board))

                                win_flag = find_winner(board)
                                if win_flag:
                                    if "Tie" != win_flag:
                                        result = f"The winner is {player2[0]}!"
                                        player1[3] += 1
                                        # win_results[j][i] = 1
                                        # win_results[i][j] = -1
                                        # print(win_results)
                                    else:
                                        result = f"They are {win_flag}!"
                                        player1[5] += 1
                                    print(result)
                                    break
                            db_execute_query("UPDATE students SET win = ?, lose = ?, tie = ? WHERE student_id = ?", (player1[2], player1[3], player1[5], player1[0]))
                        bar.progress((i+1)*100//(student_num))
                        time.sleep(0.1)
                    # Update the database
                    # print(win_results)
                    # for k in range(student_num):
                    #     win_num = win_results[k].count(1)
                    #     lose_num = win_results[k].count(-1)
                    #     student = student_records[k]
                    #     db_execute_query("UPDATE students SET win = ?, lose = ? WHERE student_id = ?", (win_num, lose_num, student[0])) 
                    st.success("Refresh successfully!") 
    
    # leaderboard display
    student_records = db_select_query("SELECT * FROM students ORDER BY win - lose DESC")
    table_data = []
    for record in student_records:
        table_data.append((record[0], record[2], record[3], record[5]))
    win_lose_result = pd.DataFrame(table_data, columns=("Student ID", "Win", "Lose", "Tie"), index=[i+1 for i in range(student_num)])
    st.table(win_lose_result)