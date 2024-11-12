from Assignment import Assignment

# Specific project managed by the company
# Attributes: projectCode, projectName, department (indicating the department overseeing the project)
# and a manager (an employee responsible for overseeing the project), a list of employees assigned to the project
class Project:
    all_projects = []

    def __init__(self, projectCode, projectName, department, manager, employees):
        self.projectCode = projectCode
        self.projectName = projectName
        self.department = department
        self.manager = manager
        self.employees = employees
        self.assigned_employees = []
        Project.all_projects.append(self)


    def assign_employee(self, employee, role, hoursWorked, startDate, endDate):
        assignment = Assignment(employee, self, role, hoursWorked, startDate, endDate)
        self.assigned_employees.append(employee)
        employee.add_assignment(assignment)


    @classmethod
    def search_by_property(cls, value):
        found = False
        for project in cls.all_projects:
            for attr, attr_value in project.__dict__.items():
                if attr_value == value:
                    print("Project Code: " + project.projectCode + ", Project Name: " + project.projectName)
                    found = True
                    break
        if not found:
            print("No projects found...")
