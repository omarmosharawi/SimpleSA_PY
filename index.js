const sqlite3 = require('sqlite3').verbose();
const readline = require('readline');
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.on("SIGINT", function () {
    console.log("\nExiting...");
    process.exit(0); // Ctrl-C
    })

async function getInput(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

let db = new sqlite3.Database('school.db', async (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Connected to school database.');

  // Call the main function after the database connection
  main();
});

// Tables in DB (Check and Create)
db.get('SELECT name FROM sqlite_master WHERE type="table" AND name="students"', (err, row) => {
    if (err) {
        console.error(err.message);
    } else {
        if (row) {
            // console.log("The students table exists.");
    }    else {
            db.run('CREATE TABLE students (student_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, nickname TEXT, age INTEGER NOT NULL, class TEXT NOT NULL, date_of_registration DATE NOT NULL, lesson_id INTEGER, FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id))',
            function (err){
                if(err){
                    return console.error(err.message);
                }
                console.log('Students table is created.');
            });
      }
    }
});

db.get('SELECT name FROM sqlite_master WHERE type="table" AND name="lessons"', (err, row) => {
    if (err) {
        console.error(err.message);
    } else {
        if (row) {
            // console.log("The lessons table exists.");
    }   else {
            db.run('CREATE TABLE lessons (lesson_id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_name TEXT NOT NULL)',
            function (err){
                if(err){
                    return console.error(err.message);
                }
                console.log('Lessons table is created.');
            });
    }
    }
});

// App Functions
async function AddStudent() {
    // const studentID = rl.prompt("Enter the student ID: ");
    const name = await getInput("Enter the student name: ");
    const nickname = await getInput("Enter the nickname: ");
    const age = parseInt(await getInput("Enter the age: "));
    const level = await getInput("Enter the class: ");
    const dateOfRegistration = await getInput("Enter the date of registration (YYYY-MM-DD): ");

    // const getLessons = [];
    // do {
    // const lesson_name = await getInput("Enter the lesson the student is studying: ");
    // if (lesson_name !== "q") {
    //     getLessons.push(lesson_name);
    // }
    // } while (lesson_name !== "q");

    const lesson_name = await getInput("Enter the lesson the student is studying: ")

    if (age === '' || name === '') {
      console.log("Cann't be empty.");
      return;
    }

  db.run('INSERT INTO students (name, nickname, age, class, date_of_registration) VALUES ( ?, ?, ?, ?, ?)', [name, nickname, age, level, dateOfRegistration]);
  db.all('SELECT * FROM students JOIN lessons ON students.lesson_id = lessons.lesson_id ');
    // db.run('INSERT INTO lessons (lesson_name) VALUES (?)', [lesson_name])
    // const lessonId = db.all('SELECT lesson_id FROM lessons WHERE lesson_name=?', [lesson_name]);
    // db.run('UPDATE students SET lesson_id=? WHERE student_id=?', [lessonId, studentID]);

// Check if the lesson exists
    const lessonExists = db.all('SELECT * FROM lessons WHERE lesson_name = ?', [lesson_name]);
    if (lessonExists.length === 0) {
        // If the lesson don't exist, create it.
        db.run('INSERT INTO lessons (lesson_name) VALUES (?)', [lesson_name]);
    }
    // Get the lesson ID
    const getLessonId = db.all('SELECT lesson_id FROM lessons WHERE lesson_name=?', [lesson_name]);
    // Update the student's lesson ID
    db.run('UPDATE students SET lesson_id=?', [getLessonId]);

    return console.log("The student has been added.");
}

async function DeleteStudent() {
    const studentID = await getInput("Enter the student ID: ");
    const ifStudent = db.all('SELECT * FROM students WHERE student_id = ?', [studentID]);

    if(ifStudent){
        db.run('DELETE FROM students WHERE student_id = ?', [studentID]);
        console.log("The student has been deleted.");
    } else{
        console.log("There's no such a student with id " , [studentID]);
    }

}

async function ModifyStudentInformation() {
    const studentID = await getInput("Enter the student ID: ");
    const name = await getInput("Enter the new name: ");
    const nickname = await getInput("Enter the new nickname: ");
    const age = await getInput("Enter the new age: ");
    const level = await getInput("Enter the new class: ");
    const dateOfRegistration = await getInput("Enter the new date of registration (YYYY-MM-DD): ");
    const lesson_id = await getInput("Enter the new lesson id the student is studying: ")

    db.run('UPDATE students SET name = ?, nickname = ?, age = ?, class = ?, date_of_registration = ?, lesson_id = ? WHERE student_id = ?', [name, nickname, age, level, dateOfRegistration, lesson_id, studentID]);

    return console.log("The student information has been updated.");
}

// async function ViewStudentInformation() {
//     const studentID = await getInput("Enter the student ID: ");

//     const result1 = db.all('SELECT * FROM students WHERE student_id = ?', [studentID]);
//     const result2 = db.all('SELECT * FROM students JOIN lessons ON students.lesson_id = lessons.lesson_id WHERE student_id = ?', [studentID]);
//     const students = result1[0];

//     if (result1 !== 0 || result2 !== 0) {
//         console.log("Name: " , students.name);
//         console.log("Nickname: " , students.nickname);
//         console.log("Age: " , students.age);
//         console.log("Class: " , students.class);
//         console.log("Date of registration: " , students.date_of_registration);
//         console.log("Lessons: " , lessons.lesson_name);
//     } else {
//         console.log("Student not found!");
//     }
// }
async function ViewStudentInformation() {
    // Get the student ID from the user
    const studentID = await getInput("Enter the student ID: ");

    // Query the database for the student
    const result = db.all('SELECT * FROM students JOIN lessons ON students.lesson_id = lessons.lesson_id WHERE student_id = ?', [studentID]);
    const student = result[0];

    // Check if the student exists
    if (result.length === 0) {
      console.log("The student does not exist.");
      return;
    }

    console.log("Student information:");
    console.log(`ID:  ${student.student_id}`)
    console.log(`Name: ${student.name}`);
    console.log(`Nickname: ${student.nickname}`);
    console.log(`Age: ${student.age}`);
    console.log(`Class: ${student.class}`);
    console.log(`Date Of Registration: ${student.date_of_registration}`);
    console.log(`Lessons: ${student.lesson_id}`)

    // name = db.get('SELECT name FROM students');
    // nickname = db.get('SELECT nickname FROM students');
    // age = db.get('SELECT age FROM students');
    // level = db.get('SELECT class FROM students');
    // dateOfReg= db.get('SELECT date_of_registration FROM students');
    // lesson_name = db.get('SELECT lesson_name FROM lessons')

    // // Print the student information
    // console.log("Student information:");
    // console.log("ID: ", student_id);
    // console.log("Name:", name);
    // console.log("Nickname:", nickname);
    // console.log("Age:", age);
    // console.log("Class:", level);
    // console.log("Date of registration:", dateOfReg);
    // console.log("Lesson:", lesson_name);
  }
//   async function ViewStudentInformation() {
//     // Get the student ID from the user.
//     const studentID = await getInput("Enter the student ID: ");

//     // Query the database for the student information.
//     const student = db.all('SELECT * FROM students WHERE student_id = ?', [studentID]);

//     // If the student does not exist, return an error message.
//     if (student.length === 0) {
//       console.log("The student does not exist.");
//       return;
//     }

//     // Print the student information to the console.
//     console.log(`Student name: ${student[0].name}`);
//     console.log(`Nickname: ${student[0].nickname}`);
//     console.log(`Age: ${student[0].age}`);
//     console.log(`Class: ${student[0].class}`);
//     console.log(`Date of registration: ${student[0].date_of_registration}`);
//     console.log(`Lesson: ${student[0].lesson_name}`);
//   }




// Main Function
async function main() {
  console.log("\n|||=== Welcome To School system administration by Omar M. Sharawi ===|||\n");

  console.log("# Please choose the operation you want to perform:");
  console.log("- To add a student, input the letter (a)");
  console.log("- To delete a student, input the letter (d)");
  console.log("- To modify a student's information, input the letter (u)");
  console.log("- To view student information, input the letter (s)");
  console.log("- To exit the App, input the letter (q) or press (Ctrl+C)");

  await getAnswer();

  // Close the database connection after all operations are done
//   db.close((err) => {
//     if (err) {
//       return console.error(err.message);
//     }
//     console.log('The database has been disconnected.');
//   });
}

async function getAnswer() {
    const answer = await getInput("Enter an operation: ");
  switch (answer) {
    case "a":
        AddStudent();
        break;
    case "d":
        DeleteStudent();
        break;
    case "u":
        ModifyStudentInformation();
        break;
    case "s":
        ViewStudentInformation();
        break;
    case "q":
        console.log("\nThank You for using our software!\n");
        db.close((err) => {
            if (err) {
              return console.error(err.message);
            }
            console.log('The database has been disconnected.');
          });
        break;
    default:
      console.log("You have entered an incorrect operation!");
      break;
  }
}
