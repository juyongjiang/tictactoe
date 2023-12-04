import streamlit as st
import pandas as pd
import ast
import astor
from db_util import db_select_query, db_execute_query

admin = ['John', 'Sung', 'Jack']


def recover_source_code(source):
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        return None
    
    return astor.to_source(tree)

st.title("View & Reset Database")
st.warning(":cop: Only admin has permission to view and reset the database:exclamation::exclamation::exclamation:")

cols = st.columns(2)
with cols[0]:
    student_id = st.text_input("Student ID:", key="student_id")
with cols[1]:
    passcode = st.text_input("Password:", type="password", key="password")

## header two columns
cols = st.columns(2)
with cols[0]:
    view_db = st.button("View All Records")
with cols[1]:
    delete_db = st.button("Delete All Records")
 
if view_db:
    if not student_id:
        st.error("Student ID cannot be empty.")
        st.stop()
    if not passcode:
        st.error("Password cannot be empty.")
        st.stop() 
    student_data = db_select_query('SELECT * FROM students WHERE student_id=?', (student_id,)) # return a list
    if len(student_data)!=0 and student_id in admin:  
        if passcode == student_data[0][4]:
            student_records = db_select_query("SELECT * FROM students")
            student_num = len(student_records)
            print(student_records)
            table_data = []
            for record in student_records:
                table_data.append((record[0], recover_source_code(record[1]), record[4]))
                print(record[1])
            win_lose_result = pd.DataFrame(table_data, columns=("Student ID", "Uploaded Code", "Password"), index=[i+1 for i in range(student_num)])
            st.table(win_lose_result)
        else:
            st.error("Incorrect passcode, please try again!")
    else:
        st.error("Permission denied!")          
    
if delete_db:
    if not student_id:
        st.error("Student ID cannot be empty.")
        st.stop()
    if not passcode:
        st.error("Password cannot be empty.")
        st.stop()
    student_data = db_select_query('SELECT * FROM students WHERE student_id=?', (student_id,)) # return a list
    if len(student_data) != 0 and student_id in admin:
        if passcode == student_data[0][4]:
            db_execute_query("DELETE FROM students")
            st.success("Database reset successfully!")
        else:
            st.error("Incorrect passcode, please try again!")
    else:
        st.error("Permission denied!")