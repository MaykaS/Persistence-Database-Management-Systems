import atexit
import sqlite3
import sys
import os

data_base_existed = os.path.isfile("schedule.db")

dbcon = sqlite3.connect("schedule.db")
cursor = dbcon.cursor()


def close_db():
    dbcon.commit()
    dbcon.close()


atexit.register(close_db)


def create_tables():
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses(
                id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL,
                student TEXT NOT NULL,
                number_of_students INTEGER NOT NULL,
                class_id INTEGER REFERENCES classrooms(id),
                course_length INTEGER NOT NULL
                )""")

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS students(
                grade TEXT PRIMARY KEY,
                count INTEGER NOT NULL
                )""")

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS classrooms(
                id INTEGER PRIMARY KEY,
                location TEXT NOT NULL,
                current_course_id INTEGER NOT NULL,
                current_course_time_left INTEGER NOT NULL
                )""")


def insert_into_db(arg):
    with open(arg) as input_file:
        for line in input_file:
            line_values = line.strip().split(',')
            for i in range(0, len(line_values)):
                line_values[i] = line_values[i].strip()

            if line_values[0] is 'C':
                cursor.execute(""" 
                INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length)
                VALUES(?,?,?,?,?,?)
                """,(line_values[1], line_values[2], line_values[3],
                      line_values[4], line_values[5], line_values[6]))

            elif line_values[0] is 'S':
                cursor.execute( """
                INSERT INTO students (grade, count) VALUES (?, ?)
                """, (line_values[1], line_values[2]) )

            elif line_values[0] is 'R':
                cursor.execute("""
                INSERT INTO classrooms (id, location, current_course_id, current_course_time_left) 
                VALUES(?,?,?,?)
                """, (line_values[1], line_values[2], 0, 0) )


def get_courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return courses


def print_course_table():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    print("courses")
    for item in courses:
        print(item)


def print_classroom_table():
    cursor.execute("SELECT * FROM classrooms")
    classrooms = cursor.fetchall()
    print("classrooms")
    for item in classrooms:
        print(item)


def print_student_table():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print("students")
    print("students")
    for item in students:
        print(item)


def main(args):
        input_file_name = args[1]
        if not data_base_existed:  # First time creating the database. Create the tables
            create_tables()
            insert_into_db(input_file_name)

        print_course_table()
        print_classroom_table()
        print_student_table()


if __name__ == '__main__':
    main(sys.argv)
