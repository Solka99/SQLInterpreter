import sqlite3

def connect_db():
    conn = sqlite3.connect('students.db')  # Podaj ścieżkę do pliku bazy danych
    return conn

def execute_query(query):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        return {"columns": columns, "rows": rows}
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()