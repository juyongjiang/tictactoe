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
    student_id = st.text_input("Admin ID:", key="student_id")
with cols[1]:
    passcode = st.text_input("Password:", type="password", key="password")

## header two columns
cols = st.columns(2)
with cols[0]:
    cols_inter = st.columns(2)
    with cols_inter[0]:
        view_db = st.button("View All Records")
        # separate = st.checkbox('Separate', value=True)
    with cols_inter[1]:
        # integrate = st.checkbox("Integrate")
        display_way = st.radio("Display Way:", ("Separate", "Integrate"), horizontal=False, index=0)
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
            student_records = db_select_query("SELECT * FROM students ORDER BY win DESC")
            student_num = len(student_records)
            print(student_records)
            table_data = []
            all_code = ""
            for record in student_records:
                table_data.append((record[0], recover_source_code(record[1]), record[4]))
                print(record[1])
                if display_way == 'Separate':
                    st.markdown(f"#### {record[0]} - {record[4]}")
                    st.code(record[1], language='python')
                all_code += f'#=================>>> {record[0]} - {record[4]} <<<=================\n\n' + record[1] + "\n"
            if display_way == 'Integrate':
                st.code(all_code, language='python')
            win_lose_result = pd.DataFrame(table_data, columns=("Student ID", "Uploaded Code", "Password"), index=[i+1 for i in range(student_num)])
            # st.table(win_lose_result)
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