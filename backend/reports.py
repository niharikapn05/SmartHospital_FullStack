from collections import Counter

from hospital import Hospital


def generate_daily_report(
    hospital: Hospital,
    date: str
) -> None:

    appointments = [
        appointment
        for appointment in hospital.appointments
        if appointment.date == date
    ]

    print("\n==============================")
    print("      DAILY APPOINTMENT REPORT")
    print("==============================")

    print(f"Date: {date}")
    print(f"Total Appointments: {len(appointments)}")

    status_count = Counter(
        appointment.status
        for appointment in appointments
    )

    print(f"Booked: {status_count.get('Booked', 0)}")
    print(f"Cancelled: {status_count.get('Cancelled', 0)}")

    print("\nAppointment Details:")

    for appointment in appointments:

        print(
            f"{appointment.patient.name} -> "
            f"{appointment.doctor.name} "
            f"({appointment.time}) "
            f"[{appointment.status}]"
        )