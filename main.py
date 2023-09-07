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

import re
def validate_string(input):
  match = re.match(r"^\D*$", input)
  if match:
    return True
  else:
    return False

import datetime
min_date = datetime.date(2000, 1, 1)
max_date = datetime.date(2023, 12, 31)


conn = sqlite3.connect("school.db", timeout=10)
if conn is None:
    print("Error: Could not connect to school database.")
else:
    print("Connected to school database.")



cursor = conn.cursor()
t1 = """CREATE TABLE IF NOT EXISTS students (student_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, nickname TEXT NOT NULL, age INTEGER NOT NULL, class TEXT NOT NULL, date_of_registration DATE NOT NULL, lesson_id INTEGER, FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id))"""
try:
  cursor.execute(t1)
  conn.commit()
except Exception as e:
  print('Error:', e, '\n')

t2 = """CREATE TABLE IF NOT EXISTS lessons (lesson_id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_name TEXT NOT NULL)"""
try:
  cursor.execute(t2)
  conn.commit()
except Exception as e:
  print('Error:', e, '\n')
lessonsData = [('Arabic',), ('English',), ('Frensh',), ('MATH',), ('Sciences',), ('Social Studies',)]
for lessons in lessonsData:
  lesson_name = lessons[0]
  cursor.execute("SELECT * FROM lessons WHERE lesson_name = ?", (lesson_name,))
  result2 = cursor.fetchone()
  if result2 is None:
    cursor.executemany("INSERT INTO lessons (lesson_name) VALUES (?)", lessonsData)
    conn.commit()

t3 = """CREATE TABLE IF NOT EXISTS classes (class_id INTEGER PRIMARY KEY AUTOINCREMENT, class_name TEXT NOT NULL)"""
try:
  cursor.execute(t3)
  conn.commit()
except Exception as e:
  print('Error:', e, '\n')
classesData = [('KG1',), ('KG2',), ('G1',), ('G2',), ('G3',), ('G4',), ('G5',), ('PREP1',), ('PREP2',), ('PREP3',)]
for classes in classesData:
  class_name = classes[0]
  cursor.execute("SELECT * FROM classes WHERE class_name = ?", (class_name,))
  result1 = cursor.fetchone()
  if result1 is None:
    cursor.executemany("INSERT INTO classes (class_name) VALUES (?)", classesData)
    conn.commit()



def AddStudent():
  while True:

    while True:
      name = input("\nEnter the student name to add: ")
      if name == "":
        print("Can't be empty! Please enter the name.")
        continue
      else:
        if validate_string(name):
          break
        else:
          print("Invalid name! Please enter a string.")
          continue

    while True:
      nickname = input("Enter the nickname: ")
      if nickname == "":
        print("Can't be empty! Please enter the nickname.")
        continue
      else:
        if validate_string(nickname):
          break
        else:
          print("Invalid nickname! Please enter a string.")
          continue

    while True:
      age = input("Enter the age: ")
      if age == "":
        print("Can't be empty! Enter the age.")
        # continue
      else:
        try:
          age = int(age)
          if (age<=17):
            pass
          else:
            print("He\She is too old to add a student older than 17 to our school.")
            continue
          break
        except ValueError:
          print("Invalid age! Please enter an integer.")
          # continue

    print("Available school classes: [KG1 - KG2 - G1 - G2 - G3 - G4 - G5 - PREP1 - PREP2 - PREP3]")
    while True:
      level = input("Enter the class: ")
      cursor.execute("SELECT * FROM classes WHERE class_name = ?", (level,))
      classExists = cursor.fetchall()
      if len(classExists) == 0:
        print("This class don't exists! Please enter from available classes only.")
        conn.commit()
        continue
      else:
        break

    while True:
        dateOfRegistration = input("Enter the date of registration (YYYY-MM-DD): ")
        if dateOfRegistration == "":
          print ("can't be empty!")
          continue
        else:
          try:
              date = datetime.datetime.strptime(dateOfRegistration, "%Y-%m-%d").date()
              if not (min_date <= date <= max_date):
                  raise ValueError
          except ValueError:
              print("Invalid date! Please enter a valid date between 2000-01-01 and 2023-12-31.")
              continue
          else:
              break

    print("Available lessons: [Arabic - English - Frensh - MATH - Sciences - Social Studies]")
    while True:
      lesson = input("Enter the lesson the student is studying: ")
      cursor.execute("SELECT * FROM lessons WHERE lesson_name = ?", (lesson,))
      lessonExists = cursor.fetchall()
      if len(lessonExists) == 0:
        print("This lesson don't exists! Please enter from available lessons only.")
        conn.commit()
        continue
      else:
        break

    addStudent = "INSERT INTO students (name, nickname, age, class, date_of_registration) VALUES (?, ?, ?, ?, ?)"
    studentValues = (name, nickname, age, level, dateOfRegistration)
    conn.execute(addStudent, studentValues)
    conn.commit()

    cursor.execute("SELECT lesson_id FROM lessons WHERE lesson_name = ?", (lesson,))
    lesson_id = cursor.fetchone()[0]

    updateStudent = "UPDATE students SET lesson_id = ? WHERE name = ?"
    studentValues = (lesson_id, name)
    conn.execute(updateStudent, studentValues)
    conn.commit()

    print("The student has been added.")



def DeleteStudent():
  while True:
    studentID = input("\nEnter the student ID to delet: ")

    cursor.execute("SELECT * FROM students WHERE student_id = ?", (studentID,))
    student = cursor.fetchone()
    if student is None:
      print("The student does not exist.")
      continue

    sql = "DELETE FROM students WHERE student_id = ?"
    values = (studentID,)
    conn.execute(sql, values)
    conn.commit()

    print("The student has been deleted.")



def ModifyStudentInformation():
  while True:
    studentID = input("\nEnter the student ID to edit the student: ")

    cursor.execute("SELECT * FROM students WHERE student_id = ?", (studentID,))
    student = cursor.fetchone()
    if student is None:
      print("The student does not exist.")
      continue

    print("- If you want to skip data without editing, you can press Enter to skip.")

    while True:
      name = input("Enter the new name: ")
      if name == "":
            break
      else:
        if validate_string(name):
          pass
        else:
          print("Invalid name! Please enter a string.")
          continue
        conn.execute("UPDATE students SET name = ? WHERE student_id = ?", (name, studentID))
        conn.commit()
        break

    while True:
      nickname = input("Enter the new nickname: ")
      if nickname == "":
            break
      else:
        if validate_string(nickname):
          pass
        else:
          print("Invalid nickname! Please enter a string.")
          continue
        conn.execute("UPDATE students SET nickname = ? WHERE student_id = ?", (nickname, studentID))
        conn.commit()
        break

    while True:
      age = input("Enter the new age: ")
      if age == "":
        break
      else:
        try:
          age = int(age)
          if age <= 17:
            pass
          else:
            print("He\She is too old to edit a student older than 17 to our school. This not allow!")
            continue
          conn.execute("UPDATE students SET age = ? WHERE student_id = ?", (age, studentID))
          conn.commit()
          break
        except ValueError:
          print("Invalid age! Please enter an integer.")
          continue

    while True:
      print("Available school classes: [KG1 - KG2 - G1 - G2 - G3 - G4 - G5 - PREP1 - PREP2 - PREP3]")
      level = input("Enter the new class: ")
      if level == "":
            break
      else:
        cursor.execute("SELECT * FROM classes WHERE class_name = ?", (level,))
        classExists = cursor.fetchall()
        if len(classExists) == 0:
            print("This class don't exists! Please enter from available classes only.")
            conn.commit()
            continue
        conn.execute("UPDATE students SET class = ? WHERE student_id = ?", (level, studentID))
        conn.commit()
        break

    while True:
      dateOfRegistration = input("Enter the new date of registration (YYYY-MM-DD): ")
      if dateOfRegistration == "":
        break
      else:
          try:
              date = datetime.datetime.strptime(dateOfRegistration, "%Y-%m-%d").date()
              if not (min_date <= date <= max_date):
                  raise ValueError
          except ValueError:
              print("Invalid date! Please enter a valid date between 2000-01-01 and 2023-12-31.")
              continue
          else:
              conn.execute("UPDATE students SET date_of_registration = ? WHERE student_id = ?", (dateOfRegistration, studentID))
              conn.commit()
              break

    while True:
      print("Available lessons: [Arabic (1) - English (2) - Frensh (3) - MATH (4) - Sciences (5) - Social Studies (6)]")
      lesson = input("Enter the new lesson id: ")
      if lesson == "":
            break
      else:
        cursor.execute("SELECT * FROM lessons WHERE lesson_id = ?", (lesson,))
        lessonExists = cursor.fetchall()
        if len(lessonExists) == 0:
            print("This lesson id don't exists! Please enter lesson id from available lessons only.")
            conn.commit()
            continue
        conn.execute("UPDATE students SET lesson_id = ? WHERE student_id = ?", (lesson, studentID))
        conn.commit()
        break

    print("The student information has been updated.")



def ViewStudentInformation():
  while True:
    studentID = input("\nEnter the student ID to view student information: ")

    sql = "SELECT * FROM students WHERE student_id = ?"
    values = (studentID,)

    result = conn.execute(sql, values)
    student = result.fetchone()

    if student is None:
      print("The student does not exist.")
      continue

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
