from hospital import Hospital
from reports import generate_daily_report


def load_sample_data(hospital: Hospital) -> None:

    hospital.add_doctor(
        "Dr. Ravi",
        "Cardiologist"
    )

    hospital.add_doctor(
        "Dr. Priya",
        "Dermatologist"
    )

    hospital.add_doctor(
        "Dr. Anil",
        "Neurologist"
    )

    hospital.add_doctor(
        "Dr. Sneha",
        "Pediatrician"
    )


def register_patient(hospital: Hospital) -> None:

    print("\n--- Patient Registration ---")

    name = input("Patient Name: ")
    age = int(input("Age: "))
    phone = input("Phone: ")

    emergency_input = input(
        "Emergency case? (yes/no): "
    )

    emergency = (
        emergency_input.lower() == "yes"
    )

    patient = hospital.register_patient(
        name,
        age,
        phone,
        emergency
    )

    print(
        f"\nPatient registered successfully!"
        f"\nPatient ID: {patient.patient_id}"
    )


def book_appointment(hospital: Hospital) -> None:

    print("\n--- Book Appointment ---")

    hospital.display_doctors()

    patient_id = int(
        input("\nPatient ID: ")
    )

    doctor_id = int(
        input("Doctor ID: ")
    )

    date = input(
        "Appointment Date (YYYY-MM-DD): "
    )

    time = input(
        "Appointment Time: "
    )

    appointment = hospital.book_appointment(
        patient_id,
        doctor_id,
        date,
        time
    )

    if appointment:

        print(
            "\nAppointment booked successfully!"
        )

        print(
            f"Appointment ID: "
            f"{appointment.appointment_id}"
        )

    else:

        print(
            "\nUnable to book appointment."
        )


def main():

    hospital = Hospital()

    load_sample_data(hospital)

    while True:

        print("\n")
        print("==============================")
        print(" SMART HOSPITAL SYSTEM")
        print("==============================")

        print("1. Register Patient")
        print("2. Display Doctors")
        print("3. Search Doctor")
        print("4. Book Appointment")
        print("5. Display Appointments")
        print("6. Patient Queue")
        print("7. Call Next Patient")
        print("8. Cancel Appointment")
        print("9. Reschedule Appointment")
        print("10. Daily Report")
        print("0. Exit")

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "1":

            register_patient(hospital)

        elif choice == "2":

            hospital.display_doctors()

        elif choice == "3":

            specialization = input(
                "Enter specialization: "
            )

            doctors = hospital.search_doctor(
                specialization
            )

            print("\nSearch Results:")

            if doctors:

                for doctor in doctors:

                    print(
                        f"{doctor.doctor_id}. "
                        f"{doctor.name} - "
                        f"{doctor.specialization}"
                    )

            else:

                print("No doctor found.")

        elif choice == "4":

            book_appointment(hospital)

        elif choice == "5":

            hospital.display_appointments()

        elif choice == "6":

            hospital.patient_queue.display()

        elif choice == "7":

            patient = hospital.call_next_patient()

            if patient:

                print(
                    f"\nNext Patient: "
                    f"{patient.name}"
                )

                print(
                    f"Priority: "
                    f"{patient.priority.name}"
                )

            else:

                print(
                    "\nNo patients in queue."
                )

        elif choice == "8":

            appointment_id = int(
                input("Appointment ID: ")
            )

            if hospital.cancel_appointment(
                appointment_id
            ):

                print(
                    "Appointment cancelled."
                )

            else:

                print(
                    "Appointment not found."
                )

        elif choice == "9":

            appointment_id = int(
                input("Appointment ID: ")
            )

            new_date = input(
                "New Date: "
            )

            new_time = input(
                "New Time: "
            )

            if hospital.reschedule_appointment(
                appointment_id,
                new_date,
                new_time
            ):

                print(
                    "Appointment rescheduled."
                )

            else:

                print(
                    "Unable to reschedule."
                )

        elif choice == "10":

            date = input(
                "Enter date (YYYY-MM-DD): "
            )

            generate_daily_report(
                hospital,
                date
            )

        elif choice == "0":

            print(
                "\nThank you for using "
                "Smart Hospital System!"
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


if __name__ == "__main__":
    main()