from Company import Company
from Department import Department
from Employee import Employee
from Project import Project

# Employees
employee1 = Employee(1000, 'Almir')
employee2 = Employee(1001, 'Admir')
employee3 = Employee(1002, 'Selma')
employee4 = Employee(1004, 'Sara')
employee5 = Employee(1005, 'Ivana')
employee6 = Employee(1006, 'Rijalda')
employee7 = Employee(1007, 'Vladimir')
employee8 = Employee(1008, 'Mahir')
employee9 = Employee(1009, 'Josip')
employee10 = Employee(1010, 'Armin')

# Projects
project1 = Project('P-100', 'Software Design C-SIC TT', 'IT Wastewater', employee1, [])
project2 = Project('P-101', 'Software Design C-GTC TT', 'IT Garbage Disposal', employee2, [])

# Departments
it_department = Department('D-1000', 'IT', employee1)
support_department = Department('D-1001', 'Support', employee2)

# Add Projects and Employees to Departments
it_department.add_project(project1)
it_department.add_employee([employee3, employee4, employee5, employee6])
support_department.add_project(project2)
support_department.add_employee([employee7, employee8, employee9, employee10])

# Add Employees, Projects and Departments to Company
company = Company()
company.add_employees([employee1, employee2, employee3, employee4, employee5, employee6, employee7, employee8, employee9, employee10])
company.add_projects([project1, project2])
company.add_department([it_department, support_department])

# Assign Projects to Employees with Roles and Hours Worked
employee1.assign_project(project1, 'Project Manager', 120, '2023-01-01', '2023-06-01')
employee2.assign_project(project2, 'Project Manager', 100, '2023-02-01', '2023-05-01')
employee3.assign_project(project1, 'Developer', 100, '2023-02-01', '2023-05-01')
employee4.assign_project(project2, 'Developer', 100, '2023-02-01', '2023-05-01')
employee5.assign_project(project1, 'Developer', 100, '2023-02-01', '2023-05-01')
employee6.assign_project(project2, 'Developer', 120, '2023-01-01', '2023-06-01')
employee7.assign_project(project1, 'Developer', 100, '2023-02-01', '2023-05-01')
employee8.assign_project(project2, 'Developer', 100, '2023-02-01', '2023-05-01')
employee9.assign_project(project1, 'Developer', 100, '2023-02-01', '2023-05-01')
employee10.assign_project(project1, 'Developer', 100, '2023-02-01', '2023-05-01')

employees = [employee1, employee2, employee3, employee4, employee5, employee6, employee7, employee8, employee9, employee10]
departments = [it_department, support_department]


# Display Employee Assignments
print("Employee Assignments")
for employee in employees:
    employee.display_assignments()
    print("\n")


# Display Department Details
print("Departments")
for department in departments:
    department.display_department_info()
    print("\n")


# Search a Project (General)
searchTerm = input("Enter project detail: ")  # e.g. 'P-100'
Project.search_by_property(searchTerm)

# Search a Company Project
print("\nSearch a company project")
companySearchTerm = input("Enter company project detail: ") # e.g. 'P-101'
Company.display_project_info(companySearchTerm)
