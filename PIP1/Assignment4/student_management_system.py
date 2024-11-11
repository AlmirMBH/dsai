class Student:
    def __init__(self, studentID, name, currentSemester):
        self.studentID = studentID
        self.name = name
        self.currentSemester = currentSemester
        self.totalECTS = 0
        self.enrollments = []

    def generate_transcript(self):
        transcript = f"Transcript for {self.name} ({self.studentID}):\n"
        for enrollment in self.enrollments:
            course_info = f"{enrollment.course.courseName} ({enrollment.course.courseCode}), " \
                          f"Grade: {enrollment.grade}, Semester: {enrollment.semesterEnrolled}, " \
                          f"Year: {enrollment.yearEnrolled}, ECTS: {enrollment.course.ECTScredits}\n"
            transcript += course_info
        return transcript

    def enroll_in_course(self, enrollment):
        self.enrollments.append(enrollment)
        self.totalECTS += enrollment.course.ECTScredits


class Course:
    def __init__(self, courseCode, courseName, ECTScredits, teacher):
        self.courseCode = courseCode
        self.courseName = courseName
        self.ECTScredits = ECTScredits
        self.teacher = teacher
        self.enrolled_students = []

    def add_student(self, student):
        self.enrolled_students.append(student)
        student.enroll_in_course(Enrollment(self, student, "Not graded", "TBD", "TBD"))

    def get_student_list(self):
        return [student.name for student in self.enrolled_students]


class Teacher:
    def __init__(self, teacherID, name):
        self.teacherID = teacherID
        self.name = name
        self.assignedCourses = []

    def assign_course(self, course):
        self.assignedCourses.append(course)

    def view_courses(self):
        return [course.courseName for course in self.assignedCourses]

    def view_enrolled_students(self, course):
        return course.get_student_list()


class Enrollment:
    def __init__(self, course, student, grade, semesterEnrolled, yearEnrolled):
        self.course = course
        self.student = student
        self.grade = grade
        self.semesterEnrolled = semesterEnrolled
        self.yearEnrolled = yearEnrolled


class Faculty:
    def __init__(self):
        self.students = []
        self.courses = []
        self.teachers = []

    def add_student(self, student):
        self.students.append(student)

    def add_course(self, course):
        self.courses.append(course)

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def search_student(self, studentID):
        for student in self.students:
            if student.studentID == studentID:
                return student
        return None

    def search_course(self, courseCode):
        for course in self.courses:
            if course.courseCode == courseCode:
                return course
        return None

    def search_teacher(self, teacherID):
        for teacher in self.teachers:
            if teacher.teacherID == teacherID:
                return teacher
        return None

    def display_student_record(self, studentID):
        student = self.search_student(studentID)
        if student:
            return student.generate_transcript()
        else:
            return "Student not found"

    def display_course_details(self, courseCode):
        course = self.search_course(courseCode)
        if course:
            return f"Course: {course.courseName}, Teacher: {course.teacher.name}, " \
                   f"Students Enrolled: {', '.join(course.get_student_list())}"
        else:
            return "Course not found"

    def display_teacher_courses(self, teacherID):
        teacher = self.search_teacher(teacherID)
        if teacher:
            return f"Teacher: {teacher.name}, Courses: {', '.join(teacher.view_courses())}"
        else:
            return "Teacher not found"
