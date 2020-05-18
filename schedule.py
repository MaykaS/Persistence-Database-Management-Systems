import sqlite3
import os

dbcon = sqlite3.connect('schedule.db')
cursor = dbcon.cursor()


def get_courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return courses


def print_table(table):
    cursor.execute('SELECT * FROM ' + table)
    object_list = cursor.fetchall()
    print(table)
    for o in object_list:
        print(o)


def main():
    courses_number = len(get_courses())
    iteration = 0

    while courses_number > 0 and os.path.isfile('schedule.db'):

        cursor.execute("SELECT * FROM classrooms")
        classrooms = cursor.fetchall()

        for _class in classrooms:
            _class = list(_class)

            if _class[3] == 1:
                cursor.execute("SELECT * FROM courses WHERE id={}".format(_class[2]))
                course = cursor.fetchone()
                print("({}) {}: {} is done".format(iteration, _class[1], course[1]))
                cursor.execute("""UPDATE classrooms SET current_course_time_left={}
                WHERE id={}""".format(0, _class[0]))
                cursor.execute("""UPDATE classrooms SET current_course_id={} WHERE id={}""".format(0, _class[0]))
                cursor.execute("DELETE FROM courses WHERE id={}".format(_class[2]))
                courses_number -= 1
                _class[3] = 0

            if _class[3] > 1:
                cursor.execute("SELECT * FROM courses WHERE id={}".format(_class[2]))
                course = cursor.fetchone()
                print("({}) {}: occupied by {}".format(iteration, _class[1], course[1]))
                cursor.execute("""UPDATE classrooms SET current_course_time_left={} WHERE id={}
                """.format(_class[3] - 1, _class[0]))

            if _class[3] == 0:
                cursor.execute("SELECT * FROM courses WHERE class_id=({})".format(_class[0]))
                course = cursor.fetchone()
                if course is not None:
                    print("({}) {}: {} is schedule to start".format(iteration, _class[1], course[1]))
                    cursor.execute("""UPDATE classrooms SET current_course_id={} WHERE id={}
                    """.format(course[0], _class[0]))
                    cursor.execute("""UPDATE classrooms SET current_course_time_left={} WHERE id={}
                    """.format(course[5], _class[0]))
                    cursor.execute("""SELECT * FROM students WHERE grade='{}'""".format(course[2]))
                    student = cursor.fetchone()
                    cursor.execute("""UPDATE students SET count = ({}) WHERE grade=('{}')
                    """.format(student[1]-course[3], course[2]))

        print_table("courses")
        print_table("classrooms")
        print_table("students")

        iteration += 1


if __name__ == '__main__':
    main()
