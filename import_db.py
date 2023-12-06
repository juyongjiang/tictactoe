import streamlit as st
from db_util import db_execute_query


export_db_path = 'export_db.txt'

# read the export_db_path file
with open(export_db_path, 'r', encoding='utf-8') as f:
    # export_db = f.readlines()  
    # for line in export_db:
    user_code = """"""
    while True:
        line = f.readline()
        if line.startswith('#=================>>>'):
            if user_code != """""":
                # print(user_code)
                db_execute_query("INSERT INTO students VALUES (?, ?, 0, 0, ?, 0)", \
                    (student_id, user_code, passcode), database_name='student_database_exported.db')
            user_header = line.split(' ')
            student_id = user_header[1]
            passcode = user_header[3]
            user_code = """"""
        elif line == '\n':
            continue
        else:
            user_code += line
        if line == "":
            if user_code != """""":
                # print(user_code)
                db_execute_query("INSERT INTO students VALUES (?, ?, 0, 0, ?, 0)", \
                    (student_id, user_code, passcode), database_name='student_database_exported.db')
            break
    