from hospital import Hospital


def test_register_patient():

    hospital = Hospital()

    patient = hospital.register_patient(
        "Niharika",
        21,
        "9876543210"
    )

    assert patient.patient_id == 1
    assert patient.name == "Niharika"
    assert len(hospital.patients) == 1


def test_emergency_patient_priority():

    hospital = Hospital()

    hospital.register_patient(
        "Normal Patient",
        30,
        "1111111111"
    )

    emergency = hospital.register_patient(
        "Emergency Patient",
        40,
        "2222222222",
        emergency=True
    )

    next_patient = hospital.call_next_patient()

    assert next_patient.patient_id == emergency.patient_id


def test_add_doctor():

    hospital = Hospital()

    doctor = hospital.add_doctor(
        "Dr. Ravi",
        "Cardiologist"
    )

    assert doctor.doctor_id == 1
    assert doctor.specialization == "Cardiologist"


def test_search_doctor():

    hospital = Hospital()

    hospital.add_doctor(
        "Dr. Ravi",
        "Cardiologist"
    )

    hospital.add_doctor(
        "Dr. Priya",
        "Dermatologist"
    )

    result = hospital.search_doctor(
        "Cardiologist"
    )

    assert len(result) == 1
    assert result[0].name == "Dr. Ravi"


def test_book_appointment():

    hospital = Hospital()

    patient = hospital.register_patient(
        "Niharika",
        21,
        "9876543210"
    )

    doctor = hospital.add_doctor(
        "Dr. Ravi",
        "Cardiologist"
    )

    appointment = hospital.book_appointment(
        patient.patient_id,
        doctor.doctor_id,
        "2026-10-02",
        "10:00 AM"
    )

    assert appointment is not None
    assert appointment.status == "Booked"


def test_cancel_appointment():

    hospital = Hospital()

    patient = hospital.register_patient(
        "Niharika",
        21,
        "9876543210"
    )

    doctor = hospital.add_doctor(
        "Dr. Ravi",
        "Cardiologist"
    )

    appointment = hospital.book_appointment(
        patient.patient_id,
        doctor.doctor_id,
        "2026-10-02",
        "10:00 AM"
    )

    result = hospital.cancel_appointment(
        appointment.appointment_id
    )

    assert result is True
    assert appointment.status == "Cancelled"


def test_concurrent_booking():

    import threading

    from concurrency import book_appointment_task

    hospital = Hospital()

    hospital.add_doctor(
        "Dr. Ravi",
        "Cardiologist"
    )

    patient1 = hospital.register_patient(
        "Patient 1",
        25,
        "1111111111"
    )

    patient2 = hospital.register_patient(
        "Patient 2",
        30,
        "2222222222"
    )

    thread1 = threading.Thread(
        target=book_appointment_task,
        args=(
            hospital,
            patient1.patient_id,
            1,
            "2026-10-02",
            "10:00 AM"
        )
    )

    thread2 = threading.Thread(
        target=book_appointment_task,
        args=(
            hospital,
            patient2.patient_id,
            1,
            "2026-10-02",
            "10:30 AM"
        )
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert len(hospital.appointments) == 2