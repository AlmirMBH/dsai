CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    enrollment_year INT
);

CREATE TABLE Courses (
    course_id INT PRIMARY KEY,
    course_name TEXT,
    credits INT,
    semester TEXT,
    student_id INT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Insert 5 students into the Students table
INSERT INTO Students (student_id, first_name, last_name, email, enrollment_year)
VALUES 
(20457, 'Almir', 'Mustafic', 'almir.mustafic@gmail.com', 2024),
(21458, 'Michael', 'Jordan', 'mj@yahoo.com', 2022),
(22459, 'Dennis', 'Rodman', 'dr@hotmail.com', 2021),
(23460, 'Scottie', 'Pipen', 'sp@gmail.com', 2023),
(24461, 'Toni', 'Kukoc', 'tc@bulls.com', 2020);

-- Insert 3 courses and link them to students
INSERT INTO Courses (course_id, course_name, credits, semester, student_id)
VALUES 
(101, 'Programing in Python 101', 4, 'Fall 2024', 20457),
(102, 'Mathematics 101', 4, 'Fall 2024', 21458),
(103, 'Fundamental Concepts of AI 101', 4, 'Fall 2024', 22459);

-- Fetch data
SELECT * FROM Students;
SELECT * FROM Courses;

-- Update the first name of a student with student_id 21458
UPDATE Students SET first_name = 'Kobe' WHERE student_id = 21458;

-- Fetch students after the update
SELECT * FROM Students;

-- Display all courses for the student with student_id = 20457
SELECT course_name FROM Courses WHERE student_id = 20457;

-- Fetch emails of students whose student_id starts with "20"
SELECT email FROM Students WHERE student_id LIKE '20%';





