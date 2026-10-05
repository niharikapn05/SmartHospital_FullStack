from algorithms import filter_items, linear_search, sort_by_name
from models import Appointment, Doctor, Patient
from queue_manager import PatientQueue


class Hospital:

    def __init__(self):

        self.patients: list[Patient] = []
        self.doctors: list[Doctor] = []
        self.appointments: list[Appointment] = []

        self.patient_queue = PatientQueue()

        self.patient_counter = 1
        self.doctor_counter = 1
        self.appointment_counter = 1

    # -------------------------
    # PATIENT MANAGEMENT
    # -------------------------

    def register_patient(
        self,
        name: str,
        age: int,
        phone: str,
        emergency: bool = False
    ) -> Patient:

        patient = Patient(
            self.patient_counter,
            name,
            age,
            phone,
            emergency
        )

        self.patient_counter += 1

        self.patients.append(patient)
        self.patient_queue.add_patient(patient)

        return patient

    # -------------------------
    # DOCTOR MANAGEMENT
    # -------------------------

    def add_doctor(
        self,
        name: str,
        specialization: str
    ) -> Doctor:

        doctor = Doctor(
            self.doctor_counter,
            name,
            specialization
        )

        self.doctor_counter += 1

        self.doctors.append(doctor)

        return doctor

    # -------------------------
    # SEARCH DOCTOR
    # -------------------------

    def search_doctor(
        self,
        specialization: str
    ) -> list[Doctor]:

        return filter_items(
            self.doctors,
            lambda doctor:
                doctor.specialization.lower()
                == specialization.lower()
        )

    # -------------------------
    # BOOK APPOINTMENT
    # -------------------------

    def book_appointment(
        self,
        patient_id: int,
        doctor_id: int,
        date: str,
        time: str
    ) -> Appointment | None:

        patient = linear_search(
            self.patients,
            lambda p: p.patient_id == patient_id
        )

        doctor = linear_search(
            self.doctors,
            lambda d: d.doctor_id == doctor_id
        )

        if patient is None:
            return None

        if doctor is None:
            return None

        if not doctor.available:
            return None

        appointment = Appointment(
            self.appointment_counter,
            patient,
            doctor,
            date,
            time
        )

        self.appointment_counter += 1

        self.appointments.append(appointment)

        return appointment

    # -------------------------
    # CANCEL APPOINTMENT
    # -------------------------

    def cancel_appointment(
        self,
        appointment_id: int
    ) -> bool:

        appointment = linear_search(
            self.appointments,
            lambda a:
                a.appointment_id == appointment_id
        )

        if appointment is None:
            return False

        appointment.cancel()

        return True

    # -------------------------
    # RESCHEDULE
    # -------------------------

    def reschedule_appointment(
        self,
        appointment_id: int,
        new_date: str,
        new_time: str
    ) -> bool:

        appointment = linear_search(
            self.appointments,
            lambda a:
                a.appointment_id == appointment_id
        )

        if appointment is None:
            return False

        if appointment.status == "Cancelled":
            return False

        appointment.date = new_date
        appointment.time = new_time

        return True

    # -------------------------
    # GET NEXT PATIENT
    # -------------------------

    def call_next_patient(self) -> Patient | None:

        return self.patient_queue.next_patient()

    # -------------------------
    # DISPLAY DOCTORS
    # -------------------------

    def display_doctors(self) -> None:

        doctors = sort_by_name(
            self.doctors,
            lambda d: d.name
        )

        print("\n--- Doctors ---")

        for doctor in doctors:

            status = (
                "Available"
                if doctor.available
                else "Unavailable"
            )

            print(
                f"ID: {doctor.doctor_id} | "
                f"{doctor.name} | "
                f"{doctor.specialization} | "
                f"{status}"
            )

    # -------------------------
    # DISPLAY APPOINTMENTS
    # -------------------------

    def display_appointments(self) -> None:

        print("\n--- Appointments ---")

        if not self.appointments:
            print("No appointments.")
            return

        for appointment in self.appointments:

            print(
                f"ID: {appointment.appointment_id} | "
                f"Patient: {appointment.patient.name} | "
                f"Doctor: {appointment.doctor.name} | "
                f"Date: {appointment.date} | "
                f"Time: {appointment.time} | "
                f"Status: {appointment.status}"
            )