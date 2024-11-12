# Represents the entire company, managing all employees, projects, and departments
# Attributes: lists of employees, projects, and departments
# Functionality: searching specific employee, project, or department and displaying their information
class Company:
    all_projects = []

    def __init__(self):
        self.employees = []
        self.projects = []
        self.departments = []


    def add_employees(self, employees):
        if isinstance(employees, list):
            for employee in employees:
                if employee not in self.employees:
                    self.employees.append(employee)
        else:
            if employees not in self.employees:
                self.employees.append(employees)


    def add_projects(self, projects):
        if isinstance(projects, list):
            for project in projects:
                if project not in self.projects:
                    self.projects.append(project)
        else:
            if projects not in self.projects:
                self.projects.append(projects)

        for project in projects:
            Company.all_projects.append(project)


    def add_department(self, departments):
        if isinstance(departments, list):
            for department in departments:
                if department not in self.departments:
                    self.departments.append(department)
        else:
            if departments not in self.departments:
                self.departments.append(departments)


    @classmethod
    def display_project_info(cls, value):
        found = False
        for project in cls.all_projects:
            for attr, attr_value in project.__dict__.items():
                if attr_value == value:
                    print("Project Code: " + project.projectCode + ", Project Name: " + project.projectName)
                    found = True
                    break
        if not found:
            print("No projects found...")
