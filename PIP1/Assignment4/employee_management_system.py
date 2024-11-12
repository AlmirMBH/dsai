from datetime import date

# Class for Employee
class Employee:
    def __init__(self, employeeID, name):
        self.employeeID = employeeID
        self.name = name
        self.project_assignments = []  # List of Assignment instances

    def add_assignment(self, assignment):
        self.project_assignments.append(assignment)

    def display_assignments(self):
        print(f"Assignments for {self.name}:")
        for assignment in self.project_assignments:
            print(f"Project: {assignment.project.projectName}, Role: {assignment.role}, "
                  f"Hours Worked: {assignment.hoursWorked}, "
                  f"Start Date: {assignment.startDate}, End Date: {assignment.endDate}")

# Class for Project
class Project:
    def __init__(self, projectCode, projectName, department, manager):
        self.projectCode = projectCode
        self.projectName = projectName
        self.department = department
        self.manager = manager  # Employee instance
        self.assigned_employees = []  # List of Employee instances

    def assign_employee(self, employee, role, hoursWorked, startDate, endDate):
        assignment = Assignment(employee, self, role, hoursWorked, startDate, endDate)
        self.assigned_employees.append(employee)
        employee.add_assignment(assignment)

# Class for Department
class Department:
    def __init__(self, departmentCode, departmentName, headOfDepartment):
        self.departmentCode = departmentCode
        self.departmentName = departmentName
        self.headOfDepartment = headOfDepartment  # Employee instance
        self.projects = []  # List of Project instances
        self.employees = []  # List of Employee instances

    def add_project(self, project):
        self.projects.append(project)

    def add_employee(self, employee):
        if employee not in self.employees:
            self.employees.append(employee)

    def display_info(self):
        print(f"Department: {self.departmentName} (Code: {self.departmentCode})")
        print(f"Head of Department: {self.headOfDepartment.name}")
        print("\nProjects:")
        for project in self.projects:
            print(f"Project Code: {project.projectCode}, Name: {project.projectName}, "
                  f"Manager: {project.manager.name}")
        print("\nEmployees:")
        for employee in self.employees:
            print(f"Employee ID: {employee.employeeID}, Name: {employee.name}")

# Class for Assignment
class Assignment:
    def __init__(self, employee, project, role, hoursWorked, startDate, endDate):
        self.employee = employee
        self.project = project
        self.role = role
        self.hoursWorked = hoursWorked
        self.startDate = startDate
        self.endDate = endDate

# Class for Company
class Company:
    def __init__(self):
        self.employees = []  # List of Employee instances
        self.projects = []  # List of Project instances
        self.departments = []  # List of Department instances

    def add_employee(self, employee):
        self.employees.append(employee)

    def add_project(self, project):
        self.projects.append(project)

    def add_department(self, department):
        self.departments.append(department)

    def find_employee(self, employeeID):
        for employee in self.employees:
            if employee.employeeID == employeeID:
                return employee
        return None

    def find_project(self, projectCode):
        for project in self.projects:
            if project.projectCode == projectCode:
                return project
        return None

    def find_department(self, departmentCode):
        for department in self.departments:
            if department.departmentCode == departmentCode:
                return department
        return None

    def display_employee_info(self, employeeID):
        employee = self.find_employee(employeeID)
        if employee:
            print(f"Employee ID: {employee.employeeID}, Name: {employee.name}")
            employee.display_assignments()
        else:
            print("Employee not found.")

    def display_project_info(self, projectCode):
        project = self.find_project(projectCode)
        if project:
            print(f"Project Code: {project.projectCode}, Name: {project.projectName}")
            print(f"Department: {project.department.departmentName}, Manager: {project.manager.name}")
            print("Assigned Employees:")
            for employee in project.assigned_employees:
                print(f"Employee ID: {employee.employeeID}, Name: {employee.name}")
        else:
            print("Project not found.")

    def display_department_info(self, departmentCode):
        department = self.find_department(departmentCode)
        if department:
            department.display_info()
        else:
            print("Department not found.")
