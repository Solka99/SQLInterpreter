import sqlite3
from grammar import parse_sql
def connect_db():
    conn = sqlite3.connect('students.db')  # Podaj ścieżkę do pliku bazy danych
    return conn

def execute_query(query):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        parse_sql(query)
        cursor.execute(query)
        conn.commit()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        return {"columns": columns, "rows": rows}
    except SyntaxError as e:
        return {"error": str(e)}
    # except sqlite3.Error as e:
    #     return {"error": str(e)}
    finally:
        conn.close()
