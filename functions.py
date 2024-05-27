import sqlite3
from grammar import update

table_list=['students']
def connect_db():
    conn = sqlite3.connect('students.db')  # Podaj ścieżkę do pliku bazy danych
    return conn

def execute_query(query):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        curr = update()
        check_if_table_name_correct(curr)
        cursor.execute(query)
        conn.commit()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()

        return {"columns": columns, "rows": rows}
    # except sqlite3.Error as e:
    #     return {"error": str(e)}
    finally:
        conn.close()

def check_if_table_name_correct(current_table_name_):
    if current_table_name_ is None:
        return
    if current_table_name_ not in table_list:
        raise NameError("Table doesn't exist")

#Queries to test
#1 SELECT name AS student_name FROM students;
#2