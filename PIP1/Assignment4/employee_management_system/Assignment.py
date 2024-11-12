# Represents an employee’s involvement in a specific project
# Attributes: role (e.g., "developer", "project manager"), hoursWorked (total hours dedicated to the project),
# startDate, and endDate.
# Functionality: N/A
class Assignment:
    def __init__(self, employee, project, role, hoursWorked, startDate, endDate):
        self.employee = employee
        self.project = project
        self.role = role
        self.hoursWorked = hoursWorked
        self.startDate = startDate
        self.endDate = endDate