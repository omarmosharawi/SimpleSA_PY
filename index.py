import sqlite3

import signal
import sys
def exit_on_ctrl_c(signum, frame):
  print("\n\nExiting...")
  print("\n# Thank You for using our software ^_^\n")
  conn.close()
  print("The database has been disconnected.")
  sys.exit(0)
signal.signal(signal.SIGINT, exit_on_ctrl_c)



conn = sqlite3.connect("school.db", timeout=10)
if conn is None:
    print("Error: Could not connect to school database.")
else:
    print("Connected to school database.")



cursor = conn.cursor()
sql1 = """CREATE TABLE IF NOT EXISTS students (student_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, nickname TEXT, age INTEGER NOT NULL, class TEXT, date_of_registration DATE NOT NULL, lesson_id INTEGER, FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id) )"""
try:
  cursor.execute(sql1)
  conn.commit()
except Exception as e:
  print('Error:', e, '\n')
sql2 = """CREATE TABLE IF NOT EXISTS lessons (lesson_id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_name TEXT NOT NULL)"""
try:
  cursor.execute(sql2)
  conn.commit()
except Exception as e:
  print('Error:', e, '\n')



def AddStudent():
  name = input("Enter the student name: ")
  nickname = input("Enter the nickname: ")
  age = int(input("Enter the age: "))
  level = input("Enter the class: ")
  dateOfRegistration = input("Enter the date of registration (YYYY-MM-DD): ")

  addStudent = "INSERT INTO students (name, nickname, age, class, date_of_registration) VALUES (?, ?, ?, ?, ?)"
  studentValues = (name, nickname, age, level, dateOfRegistration)
  conn.execute(addStudent, studentValues)
  conn.commit()

#   lesson = input("Enter the lesson the student is studying: ")
#   addLesson = "INSERT INTO lessons (lesson_name) VALUES (?)"
#   lessonValue = (lesson)
#   conn.execute(addLesson, lessonValue)
#   conn.commit()

  lesson = input("Enter the lesson the student is studying: ")
  cursor.execute("SELECT * FROM lessons WHERE lesson_name = ?", (lesson,))
  lessonExists = cursor.fetchall()
  if len(lessonExists) == 0:
        addLesson = "INSERT INTO lessons (lesson_name) VALUES (?)"
        lessonValue = (lesson,)
        cursor.execute(addLesson, lessonValue)
        conn.commit()

  cursor.execute("SELECT lesson_id FROM lessons WHERE lesson_name = ?", (lesson,))
  lesson_id = cursor.fetchone()[0]

  updateStudent = "UPDATE students SET lesson_id = ? WHERE name = ?"
  studentValues = (lesson_id, name)
  conn.execute(updateStudent, studentValues)
  conn.commit()

  # # Take the lesson names from the user and store them in a list
  # lessons = []
  # while True:
  #   lesson = input("Enter the lessons the student is studying (enter 'q' when finished): ")
  #   if lesson == "q":
  #     break
  #   else:
  #     lessons.append(lesson)

  # # For each lesson in the list
  # for lesson in lessons:
  #   # Check if the lesson exists in the lessons table
  #   cursor.execute("SELECT * FROM lessons WHERE lesson_name = ?", (lesson,))
  #   lessonExists = cursor.fetchall()

  #   # If not, insert the lesson into the lessons table
  #   if len(lessonExists) == 0:
  #     addLesson = "INSERT INTO lessons (lesson_name) VALUES (?)"
  #     lessonValue = (lesson,)
  #     try:
  #       cursor.execute(addLesson, lessonValue)
  #       conn.commit()
  #     except Exception as e:
  #       print("Error while adding lesson: ", e)
  #       return

  # # Update the student record with the lesson ids using a join query
  # updateStudent = "UPDATE students SET lesson_id = (SELECT GROUP_CONCAT(lesson_id) FROM lessons WHERE lesson_name IN (?)) WHERE name = ?"
  # studentValues = (",".join(lessons), name)
  # try:
  #   conn.execute(updateStudent, studentValues)
  #   conn.commit()
  # except Exception as e:
  #   print("Error while updating lesson_id in the students table: ", e)
  #   return

  print("The student has been added.")



def DeleteStudent():
  studentID = input("Enter the student ID: ")

  cursor.execute("SELECT * FROM students WHERE student_id = ?", (studentID,))
  student = cursor.fetchone()
  if student is None:
    print("The student does not exist.")
    return

  sql = "DELETE FROM students WHERE student_id = ?"
  values = (studentID,)
  conn.execute(sql, values)
  conn.commit()

  print("The student has been deleted.")



def ModifyStudentInformation():
  studentID = input("Enter the student ID: ")

  cursor.execute("SELECT * FROM students WHERE student_id = ?", (studentID,))
  student = cursor.fetchone()
  if student is None:
    print("The student does not exist.")
    return

  print("- If you want to skip data without editing, you can press Enter to skip.")
  name = input("Enter the new name: ")
  nickname = input("Enter the new nickname: ")
  age = input("Enter the new age: ")
  level = input("Enter the new class: ")
  dateOfRegistration = input("Enter the new date of registration (YYYY-MM-DD): ")
  lesson = input("Enter the new lesson id: ")


  if name == "":
    pass
  else:
    conn.execute("UPDATE students SET name = ? WHERE student_id = ?", (name, studentID))
    conn.commit()
  if nickname == "":
    pass
  else:
    conn.execute("UPDATE students SET nickname = ? WHERE student_id = ?", (nickname, studentID))
    conn.commit()
  if age == "":
    pass
  else:
    conn.execute("UPDATE students SET age = ? WHERE student_id = ?", (age, studentID))
    conn.commit()
  if level == "":
    pass
  else:
    conn.execute("UPDATE students SET class = ? WHERE student_id = ?", (level, studentID))
    conn.commit()
  if dateOfRegistration == "":
    pass
  else:
    conn.execute("UPDATE students SET date_of_registration = ? WHERE student_id = ?", (dateOfRegistration, studentID))
    conn.commit()
  if lesson == "":
    pass
  else:
    conn.execute("UPDATE students SET lesson_id = ? WHERE student_id = ?", (lesson, studentID))
    conn.commit()

  print("The student information has been updated.")


  # sql = "UPDATE students SET name = ?, nickname = ?, age = ?, class = ?, date_of_registration = ? WHERE student_id = ?"
  # values = (name, nickname, age, level, dateOfRegistration, studentID)
  # conn.execute(sql, values)
  # conn.commit()

  # print("The student information has been updated.")



def ViewStudentInformation():
  studentID = input("Enter the student ID: ")

  sql = "SELECT * FROM students WHERE student_id = ?"
  values = (studentID,)

  result = conn.execute(sql, values)
  student = result.fetchone()

  if student is None:
    print("The student does not exist.")
    return

  print("\nStudent information:")
  print("ID =>", student[0])
  print("Name =>", student[1])
  print("Nickname =>", student[2])
  print("Age =>", student[3])
  print("Class =>", student[4])
  print("Date of registration =>", student[5])

  cursor.execute("SELECT lesson_name FROM lessons WHERE lesson_id = ?", (student[6],))
  lesson_name = cursor.fetchone()[0]
  print("Lessons =>", lesson_name)



def main():
    print("\n|||=== Welcome To School system administration by Omar M. Sharawi ===|||\n")

    print("# Please choose the operation you want to perform:")
    print("- To add a student, input the letter (a)")
    print("- To delete a student, input the letter (d)")
    print("- To modify a student's information, input the letter (u)")
    print("- To view student information, input the letter (s)")
    print("- To exit the App, input the letter (q) or press (Ctrl+C)")

    while True:
        answer = input("Enter an operation: ")

        if answer == "a":
           AddStudent()
           break
        elif answer == "d":
            DeleteStudent()
            break
        elif answer == "u":
            ModifyStudentInformation()
            break
        elif answer == "s":
            ViewStudentInformation()
            break
        elif answer == "q":
            print("\n# Thank You for using our software ^_^\n")
            conn.close()
            print("The database has been disconnected.")
            exit()
        else:
            print("Invalid operation!")



if __name__ == "__main__":
  main()
