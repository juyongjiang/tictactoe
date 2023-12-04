import streamlit as st
import random
import time
import pandas as pd
import base64
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
    print(str_board)
    return str_board

def put_a_stone(board, x, y, stone):
    if board[x][y] == 0:
        board[x][y] = stone
        return board, True
    else:
        print(f"Spot {x},{y} is already occupied. Try another spot.")
        return board, False

# set global variable to save time and memory
def random_put(board, stone):
    while True:
        x, y = random.randint(0, 2), random.randint(0, 2)
        if board[x][y] == 0:
            board[x][y] = stone
            # if initialized winner, roll back
            if find_winner(board):
                board[x][y] = 0
                continue
            break
    return board

def random_board(board):
    random_stone_num = random.randint(0, 9) # random stone number
    if random_stone_num != 0:
         for i in range(random_stone_num//2):
             random_put(board, 1)
             random_put(board, 2) 
    return board

def exchange_order(org_board):
    board = copy.deepcopy(org_board)
    for row in board:
        for i in range(len(row)):
            if row[i] == 1:
                row[i] = 2
            elif row[i] == 2:
                row[i] = 1
    return board

# TODO
# @st.cache_data
# def get_img_as_base64(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# img = get_img_as_base64("qr.jpg")

# page_bg_img = """
# <style>
# [data-testid="stAppViewContainer"] > .main {{
# background-image: url("") 
# background-size: 180%;
# background-position: top left;
# background-repeat: no-repeat;
# background-attachment: local;
# }}

# [data-testid="stHeader"]{
# background-color: rgba(0, 0, 0, 0);
# }

# [data-testid="stToolbar"]{
# right: 2rem;
# }

# [data-testid="stSidebar"] > div:first-child {{
# background-image: url("data:image/png;base64,{img}");
# background-position: center;
# }}

# </style>
# """
# st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("TTT Tournament")

student_records = db_select_query("SELECT * FROM students")
st.info(":computer: A total of {} students have participated in Tic-Tac-Toe game. Good Luck!:four_leaf_clover:".format(len(student_records)))
st.success(":balloon::balloon: If you win a round, there will be celebration balloons on the screen.:balloon::balloon:")

# Show participants
st.markdown("### Participants")
cols = st.columns(2)
with cols[0]:
    student_id = st.text_input("Student ID:", key="student_id")
with cols[1]:
    passcode = st.text_input("Password:", type="password", key="password")

all_student_ids = [record[0] for record in student_records]
try:
    all_student_ids.remove(student_id)
except:
    st.error("User does not exist, please upload code first or check student ID!")
prefix_opt = [" ", "ALL Students"]
opponent_id = st.selectbox("Opponent ID:", prefix_opt + all_student_ids, index=0)
# for record in student_records:
#     st.markdown("- {}".format(record[0]))  # record[0] is student_id

if len(student_records) < 2:
    st.warning("At least two students participated are required to start the tournament!")
else:
    random_button = st.checkbox('Random Initialized Board')
    start_tournament = st.button("Start Tournament")
    if start_tournament:
        if not student_id:
            st.error("Student ID cannot be empty.")
            st.stop()
        if not passcode:
            st.error("Password cannot be empty.")
            st.stop()
        if not opponent_id:
            st.error("Opponent ID cannot be empty.")
            st.stop()
        student_data = db_select_query('SELECT * FROM students WHERE student_id=?', (student_id,)) # return a list
        if not student_data:
            st.error("User does not exist, please upload code first or check student ID!")
        student_records_except_self = db_select_query('SELECT * FROM students WHERE student_id!=?', (student_id,))
        opponent_data = db_select_query('SELECT * FROM students WHERE student_id=?', (opponent_id,)) if opponent_id!="ALL Students" else student_records_except_self
        
        print(student_data[0][0])
        print(len(opponent_data))
        
        if passcode == student_data[0][4]:
            st.markdown("### Tournament Results")
            # show progress
            bar = st.progress(0)
            win_num, lose_num = 0, 0
            for i in range(0, len(opponent_data)):
                board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                player1 = list(student_data[0])
                player2 = list(opponent_data[i])
                st.markdown("### Round {}: {} vs {}".format(i, player1[0], player2[0]))
                print("### Round {}: {} (X) vs {} (O)".format(i, player1[0], player2[0]))
                bar.progress((i+1)*100//len(opponent_data))
                time.sleep(0.1)
                
                # for version 2 
                if random_button:
                    board = random_board(board)
                    st.markdown("**Random Initialized Board:**")
                    st.text(print_board(board))

                st.markdown("**======> Start Playing <======**")
                step = 1
                while(True):
                    st.markdown(f"--------------- Step {step} ---------------")
                    step += 1 
                    # Execute the student 1 code of next_move() function to get their choice
                    play1_code = f"{player1[1]}\nboard = {copy.deepcopy(board)}\nprint(next_move(board))"  
                    try:  
                        player1_choice, _ = execute_code(play1_code) 
                        play1_x, play1_y = eval(player1_choice) 
                    except:
                        st.write(f"{player1[0]}'s code made an Exception. {player2[0]} wins!")
                        st.text(print_board(board)) 
                        lose_num += 1
                        break

                    board, valid_move = put_a_stone(board, play1_x, play1_y, 1)
                    if not valid_move:
                        st.write(f"{player1[0]}: {player1_choice}")
                        st.error(f"{player1[0]} made an invalid move due to spot is already occupied. \
                                {player2[0]} wins!")
                        st.text(print_board(board)) 
                        lose_num += 1
                        break
                    st.write(f"{player1[0]}: {player1_choice}")
                    st.text(print_board(board))
                    
                    win_flag = find_winner(board)
                    if win_flag:
                        if "Tie" != win_flag:
                            result = f"The winner is {player1[0]}!"
                            st.balloons()
                            win_num += 1
                            st.success(result)
                        else:
                            result = f"They are {win_flag}!"
                            st.warning(result)
                        print(result, "\n")
                        break

                    # ---------------------------------------------------------------------
                    # Execute the student 2 code of next_move() function to get their choice
                    play2_code = f"{player2[1]}\nboard = {exchange_order(copy.deepcopy(board))}\nprint(next_move(board))" 
                    try:
                        player2_choice, _ = execute_code(play2_code) 
                        play2_x, play2_y = eval(player2_choice)
                    except:
                        st.write(f"{player2[0]}'s code made an Exception. {player1[0]} wins!")
                        st.text(print_board(board)) 
                        win_num += 1
                        break
                    
                    board, valid_move = put_a_stone(board, play2_x, play2_y, 2)
                    if not valid_move:
                        st.write(f"{player2[0]}: {player2_choice}")
                        st.success(f"{player2[0]} made an invalid move due to spot is already occupied. \
                                {player1[0]} wins!")
                        st.text(print_board(board)) 
                        st.balloons()
                        win_num += 1
                        break  
                    st.write(f"{player2[0]}: {player2_choice}")
                    st.text(print_board(board))

                    win_flag = find_winner(board)
                    if win_flag:
                        if "Tie" != win_flag:
                            result = f"The winner is {player2[0]}!"
                            lose_num += 1
                            st.error(result)
                        else:
                            result = f"They are {win_flag}!"
                            st.warning(result)
                        print(result, "\n")
                        break

            # Update the database
            # db_execute_query("UPDATE students SET win = ? lose = ? WHERE student_id = ?", (win_num, lose_num, student_data[0][0]))  
            st.markdown("### Tournament Standings")
            win_lose_result = pd.DataFrame([(student_data[0][0], win_num, lose_num),], columns=("Student ID", "Win", "Lose"), index=[1])
            # win_lose_result = win_lose_result.rename_axis('Rank')
            # win_lose_result.index.name = "Index"
            # win_lose_result = win_lose_result.set_index("Student ID")
            st.table(win_lose_result)
            # student_records = db_select_query("SELECT * FROM students ORDER BY win DESC")
            # for record in student_records:
            #     st.write(f"{record[0]}: {record[2]}")
        else:
            st.error("Incorrect password, please try again!")