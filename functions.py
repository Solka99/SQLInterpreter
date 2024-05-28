import sqlite3
from grammar import update

table_list=['students','COMPANY']
def connect_db():
    conn = sqlite3.connect('students.db')  # Podaj ścieżkę do pliku bazy danych
    return conn

def execute_query(query):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        curr,create = update()
        check_if_table_name_correct(curr,create)
        cursor.execute(query)
        conn.commit()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()

        return {"columns": columns, "rows": rows}
    # except sqlite3.Error as e:
    #     return {"error": str(e)}
    finally:
        conn.close()

def check_if_table_name_correct(current_table_name_,create_bool):
    if create_bool is True:
        table_list.append(current_table_name_)
    if current_table_name_ is None:
        return
    if current_table_name_ not in table_list:
        raise NameError("Table doesn't exist")

#Queries to test
# 1 SELECT name AS student_name FROM students;
# 2 select * from students2 where name='Kasia';
# 3 update students set major='Computer Science' where age=21; select * from students;
# 4 SELECT name, age FROM students ORDER BY age DESC;
# 5 SELECT * FROM students WHERE major LIKE 'M%';
# 6 SELECT count(*) from students where age>20; select * from students
# 7 SELECT major,avg(age) as average_age FROM students GROUP BY major;
# 8 SELECT * FROM students WHERE age = (SELECT MIN(age) FROM students) or age = (SELECT max(age) FROM students)
# 9 SELECT major, AVG(age) AS average_age
# FROM students
# GROUP BY major
# HAVING avg(age) > 20;
# 10 select students.major from students inner join COMPANY on students.id=COMPANY.id;
#11 CREATE TABLE Persons (Id int UNIQUE, Age int);


