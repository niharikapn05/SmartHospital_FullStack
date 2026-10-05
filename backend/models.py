from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    EMERGENCY = 1
    HIGH = 2
    NORMAL = 3


@dataclass
class Patient:
    patient_id: int
    name: str
    age: int
    phone: str
    emergency: bool = False

    @property
    def priority(self) -> Priority:
        return Priority.EMERGENCY if self.emergency else Priority.NORMAL


@dataclass
class Doctor:
    doctor_id: int
    name: str
    specialization: str
    available: bool = True


@dataclass
class Appointment:
    appointment_id: int
    patient: Patient
    doctor: Doctor
    date: str
    time: str
    status: str = "Booked"

    def cancel(self) -> None:
        self.status = "Cancelled"