import sqlite3

DATABASE_NAME = 'student_database.db'

def db_execute_query(query, params=None, database_name=DATABASE_NAME):
    """
    Execute a query with parameters.

    :param query: SQL query to execute.
    :param params: Optional tuple of parameters to replace within the query.
    """
    conn = None
    try:
        # Open connection
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students
                (student_id text, code text, win integer, lose integer, password text)''')
        # Execute query with parameters and commit changes
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close connection
        if conn:
            conn.close()

def db_select_query(query, params=None, database_name=DATABASE_NAME):
    """
    Execute a selection query, such as a SELECT statement.

    :param query: SQL query to execute.
    :return: Fetched results.
    """
    rows = []
    conn = None
    try:
        # Open connection
        conn = sqlite3.connect(database_name)
        c = conn.cursor()

        # Execute query and fetch results
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
            
        rows = c.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close connection
        if conn:
            conn.close()
    return rows
