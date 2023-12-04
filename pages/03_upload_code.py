import streamlit as st
from streamlit_ace import st_ace
from code_util import execute_code
from db_util import db_execute_query, db_select_query


st.title("Upload Code")
st.info(":computer: Please enter your student ID, password (initialized for the first time, after that, if you forget your password, please contact admin :cop: ), \
    and complete \"next_move(board)\" strategy that returns x, y (the position of your next piece).\
    In other words, your goal is to let \"Play 1 (You) :partying_face:\" win the game.")

cols = st.columns(2)
with cols[0]:
    student_id = st.text_input("Student ID:", key="student_id")
with cols[1]:
    passcode = st.text_input("Password:", type="password", key="password")
# student_code = st.text_area("Write program that prints out 'rock', 'scissors', or 'paper'")

# student_id = st.text_input("Student ID:")
# student_code = st.text_area("Write Code:", height=300)
# Spawn a new Ace editor
student_code = st_ace(
    auto_update=True,
    height=500,
    language="python",
    keybinding="vscode",
    show_gutter=True,
    placeholder="Write your python code here...",
    value="""### Input an board (3x3 list) as function argument, 
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

def next_move(board):\n
    return 0, 0
"""
)

basic_code = """
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
x, y = next_move(board) # x, y can't be tuple, must be int

assert x >= 0 and x <= 2
assert y >= 0 and y <= 2
"""

if st.button("Upload Code"):
    if not student_id:
        st.error("Student ID cannot be empty.")
        st.stop()
    if student_id in {'Sung', 'John', 'Jack'} or (student_id.isdigit() and len(student_id) == 8):
        if not passcode:
            st.error("Password cannot be empty.")
            st.stop()
        if not student_code:
            st.error("Student code cannot be empty.")
            st.stop()
        test_output, error = execute_code(student_code + basic_code)
        if error:
            st.error(f"Code execution failed: {error}")
        elif test_output is not None:
            st.success(f"Code execution successful: {test_output}")
            student_data = db_select_query('SELECT * FROM students WHERE student_id=?', (student_id,)) # return a list
            if not student_data:
                db_execute_query("INSERT INTO students VALUES (?, ?, 0, 0, ?)", (student_id, student_code, passcode))
                st.success(f"Welcome {student_id}! Code uploaded successfully!")
            else:
                if passcode == student_data[0][4]:
                    db_execute_query("UPDATE students SET code = ? WHERE student_id = ?", (student_code, student_id))
                    st.success("Code updated successfully!")
                else:
                    st.error("Incorrect password, please try again!")
        else:
            st.error("Code execution failed. Please check your code.")
    else:
        st.error("Student ID must be an 8-digit number!")
        st.stop()