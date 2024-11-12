from Assignment import Assignment

# Attributes: employeeID, name, list of project assignments detailing each project they've worked on
# Functionality: display all project assignments with roles and hours worked
class Employee:
    def __init__(self, employeeID, name):
        self.employeeID = employeeID
        self.name = name
        self.project_assignments = []


    def add_assignment(self, assignment):
        self.project_assignments.append(assignment)


    def assign_project(self, project, role, hoursWorked, startDate, endDate):
        assignment = Assignment(self, project, role, hoursWorked, startDate, endDate)
        self.project_assignments.append(assignment)

        if self not in project.employees:
            project.assign_employee(self, role, hoursWorked, startDate, endDate)


    def display_assignments(self):
        print("Employee: " + self.name)
        for assignment in self.project_assignments:
            print("Project: " + assignment.project.projectName +
                  ", Role: " + assignment.role +
                  ", Hours Worked: " + str(assignment.hoursWorked) +
                  " , Start Date: " + assignment.startDate +
                  ", End Date: " + assignment.endDate)
