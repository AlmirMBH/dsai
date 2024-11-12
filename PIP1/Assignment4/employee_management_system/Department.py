# Represents a department within the company, such as "IT", "Finance", or "Marketing"
# Attributes: departmentCode, departmentName, and an employee who is the headOfDepartment
# A list of all projects and employees within the department
# Functionality: display detailed information about department projects and employees
class Department:
    def __init__(self, departmentCode, departmentName, headOfDepartment):
        self.departmentCode = departmentCode
        self.departmentName = departmentName
        self.headOfDepartment = headOfDepartment
        self.projects = []
        self.employees = []


    def add_project(self, projects):
        if isinstance(projects, list):
            for project in projects:
                if project not in self.projects:
                    self.projects.append(project)
        else:
            if projects not in self.projects:
                self.projects.append(projects)


    def add_employee(self, employees):
        if isinstance(employees, list):
            for employee in employees:
                if employee not in self.employees:
                    self.employees.append(employee)
        else:
            if employees not in self.employees:
                self.employees.append(employees)


    def display_department_info(self):
        print("Department: " + self.departmentName + "(Code: " + self.departmentCode +
              "\nHead of Department: " + self.headOfDepartment.name +
              "\nProjects:")

        for project in self.projects:
            print("Project Code: " + project.projectCode +
                  ", Name: " + project.projectName +
                  ", Manager: " + project.manager.name +
                  "\nEmployees:")
        for employee in self.employees:
            print("Employee ID: " + str(employee.employeeID) + ", Name: " + employee.name)
