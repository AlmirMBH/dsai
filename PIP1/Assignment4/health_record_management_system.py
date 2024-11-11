class Patient:
    def __init__(self, patientID, name, age):
        self.patientID = patientID
        self.name = name
        self.age = age
        self.medicalHistory = []
        self.appointments = []

    def view_medical_history(self):
        return self.medicalHistory

    def update_medical_history(self, treatment):
        self.medicalHistory.append(treatment)

    def schedule_appointment(self, appointment):
        self.appointments.append(appointment)


class Doctor:
    def __init__(self, doctorID, name):
        self.doctorID = doctorID
        self.name = name
        self.assigned_patients = []

    def assign_patient(self, patient):
        self.assigned_patients.append(patient)

    def view_patient_history(self, patient):
        return patient.view_medical_history()

    def schedule_appointment(self, appointment):
        for patient in self.assigned_patients:
            if patient.patientID == appointment.patient.patientID:
                patient.schedule_appointment(appointment)
                return True
        return False


class Appointment:
    def __init__(self, appointmentID, date, time, doctor, patient):
        self.appointmentID = appointmentID
        self.date = date
        self.time = time
        self.doctor = doctor
        self.patient = patient


class Treatment:
    def __init__(self, treatmentID, description, doctor):
        self.treatmentID = treatmentID
        self.description = description
        self.doctor = doctor

    def assign_to_patient(self, patient):
        patient.update_medical_history(self)


class Clinic:
    def __init__(self):
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.treatments = []

    def add_patient(self, patient):
        self.patients.append(patient)

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def add_treatment(self, treatment):
        self.treatments.append(treatment)

    def search_patient(self, patientID):
        for patient in self.patients:
            if patient.patientID == patientID:
                return patient
        return None

    def search_doctor(self, doctorID):
        for doctor in self.doctors:
            if doctor.doctorID == doctorID:
                return doctor
        return None

    def search_appointment(self, appointmentID):
        for appointment in self.appointments:
            if appointment.appointmentID == appointmentID:
                return appointment
        return None

    def search_treatment(self, treatmentID):
        for treatment in self.treatments:
            if treatment.treatmentID == treatmentID:
                return treatment
        return None
