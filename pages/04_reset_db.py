import streamlit as st
from db_util import db_select_query, db_execute_query

admin = ['John', 'Sung', 'Jack']

st.title("Reset Database")
st.warning(":cop: Only admin has permission to reset the database:exclamation::exclamation::exclamation:")

cols = st.columns(2)
with cols[0]:
    student_id = st.text_input("Student ID:", key="student_id")
with cols[1]:
    passcode = st.text_input("Password:", type="password", key="password")

if st.button("Delete All Records"):
    if not student_id:
        st.error("Student ID cannot be empty.")
        st.stop()
    if not passcode:
        st.error("Password cannot be empty.")
        st.stop()
    student_data = db_select_query('SELECT * FROM students WHERE student_id=?', (student_id,)) # return a list
    if len(student_data) != 0 and student_id in admin:
        if passcode == student_data[4]:
            db_execute_query("DELETE FROM students")
            st.success("Database reset successfully!")
        else:
            st.error("Incorrect passcode, please try again!")
    else:
        st.error("Permission denied!")