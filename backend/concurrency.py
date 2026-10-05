import threading
import time

from hospital import Hospital


def book_appointment_task(
    hospital: Hospital,
    patient_id: int,
    doctor_id: int,
    date: str,
    appointment_time: str
) -> None:

    print(
        f"Thread {threading.current_thread().name}: "
        f"Processing patient {patient_id}"
    )

    # Simulate an I/O operation
    time.sleep(1)

    appointment = hospital.book_appointment(
        patient_id,
        doctor_id,
        date,
        appointment_time
    )

    if appointment:
        print(
            f"Thread {threading.current_thread().name}: "
            f"Appointment {appointment.appointment_id} "
            f"booked for patient {patient_id}"
        )
    else:
        print(
            f"Thread {threading.current_thread().name}: "
            f"Booking failed for patient {patient_id}"
        )


def run_concurrent_bookings() -> None:

    hospital = Hospital()

    # Add doctors
    hospital.add_doctor(
        "Dr. Ravi",
        "Cardiologist"
    )

    hospital.add_doctor(
        "Dr. Priya",
        "Dermatologist"
    )

    # Register patients
    patient1 = hospital.register_patient(
        "Rahul",
        30,
        "9000000001"
    )

    patient2 = hospital.register_patient(
        "Anjali",
        25,
        "9000000002"
    )

    patient3 = hospital.register_patient(
        "Ravi",
        40,
        "9000000003",
        emergency=True
    )

    # Create threads
    threads = [
        threading.Thread(
            target=book_appointment_task,
            args=(
                hospital,
                patient1.patient_id,
                1,
                "2026-10-02",
                "10:00 AM"
            ),
            name="Booking-1"
        ),

        threading.Thread(
            target=book_appointment_task,
            args=(
                hospital,
                patient2.patient_id,
                2,
                "2026-10-02",
                "10:30 AM"
            ),
            name="Booking-2"
        ),

        threading.Thread(
            target=book_appointment_task,
            args=(
                hospital,
                patient3.patient_id,
                1,
                "2026-10-02",
                "11:00 AM"
            ),
            name="Booking-3"
        )
    ]

    start_time = time.perf_counter()

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()

    end_time = time.perf_counter()

    print("\n--- Concurrent Booking Summary ---")

    hospital.display_appointments()

    print(
        f"\nTotal execution time: "
        f"{end_time - start_time:.2f} seconds"
    )


if __name__ == "__main__":
    run_concurrent_bookings()