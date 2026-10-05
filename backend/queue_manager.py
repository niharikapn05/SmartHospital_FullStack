import heapq
from itertools import count

from models import Patient


class PatientQueue:
    def __init__(self):
        self.queue = []
        self.counter = count()
    def add_patient(self, patient: Patient) -> None:
        entry = (
            patient.priority.value,
            next(self.counter),
            patient
        )

        heapq.heappush(self.queue, entry)

    def next_patient(self) -> Patient | None:
        if not self.queue:
            return None

        return heapq.heappop(self.queue)[2]

    def peek(self) -> Patient | None:
        if not self.queue:
            return None

        return self.queue[0][2]

    def size(self) -> int:
        return len(self.queue)

    def display(self) -> None:
        if not self.queue:
            print("Queue is empty.")
            return

        patients = sorted(self.queue)

        print("\n--- Patient Queue ---")

        for position, (_, _, patient) in enumerate(patients, 1):
            priority = patient.priority.name

            print(
                f"{position}. "
                f"{patient.name} | "
                f"ID: {patient.patient_id} | "
                f"Priority: {priority}"
            )