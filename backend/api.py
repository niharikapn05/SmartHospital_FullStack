from datetime import date as date_type
from threading import Lock
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from hospital import Hospital

app = FastAPI(
    title="Smart Hospital Appointment & Patient Queue API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hospital = Hospital()
lock = Lock()


def load_sample_data() -> None:
    if hospital.doctors:
        return
    hospital.add_doctor("Dr. Ravi", "Cardiologist")
    hospital.add_doctor("Dr. Priya", "Dermatologist")
    hospital.add_doctor("Dr. Anil", "Neurologist")
    hospital.add_doctor("Dr. Sneha", "Pediatrician")


load_sample_data()


class PatientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=130)
    phone: str = Field(min_length=7, max_length=20)
    emergency: bool = False


class DoctorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    specialization: str = Field(min_length=2, max_length=100)


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    time: str


class RescheduleRequest(BaseModel):
    new_date: str
    new_time: str


def patient_dict(p):
    return {
        "patient_id": p.patient_id,
        "name": p.name,
        "age": p.age,
        "phone": p.phone,
        "emergency": p.emergency,
        "priority": p.priority.name,
    }


def doctor_dict(d):
    return {
        "doctor_id": d.doctor_id,
        "name": d.name,
        "specialization": d.specialization,
        "available": d.available,
    }


def appointment_dict(a):
    return {
        "appointment_id": a.appointment_id,
        "patient": patient_dict(a.patient),
        "doctor": doctor_dict(a.doctor),
        "date": a.date,
        "time": a.time,
        "status": a.status,
    }


@app.get("/")
def root():
    return {"message": "Smart Hospital API is running", "docs": "/docs"}


@app.get("/api/doctors")
def get_doctors():
    return [doctor_dict(d) for d in hospital.doctors]


@app.post("/api/doctors")
def add_doctor(data: DoctorCreate):
    with lock:
        return doctor_dict(hospital.add_doctor(data.name, data.specialization))


@app.get("/api/doctors/search")
def search_doctors(specialization: str):
    return [doctor_dict(d) for d in hospital.search_doctor(specialization)]


@app.get("/api/patients")
def get_patients():
    return [patient_dict(p) for p in hospital.patients]


@app.post("/api/patients")
def register_patient(data: PatientCreate):
    with lock:
        return patient_dict(
            hospital.register_patient(
                data.name, data.age, data.phone, data.emergency
            )
        )


@app.get("/api/appointments")
def get_appointments():
    return [appointment_dict(a) for a in hospital.appointments]


@app.post("/api/appointments")
def book_appointment(data: AppointmentCreate):
    with lock:
        appointment = hospital.book_appointment(
            data.patient_id, data.doctor_id, data.date, data.time
        )
        if appointment is None:
            raise HTTPException(
                status_code=400,
                detail="Unable to book appointment. Check patient, doctor, or availability.",
            )
        return appointment_dict(appointment)


@app.patch("/api/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int):
    with lock:
        if not hospital.cancel_appointment(appointment_id):
            raise HTTPException(status_code=404, detail="Appointment not found")
        return {"message": "Appointment cancelled successfully"}


@app.patch("/api/appointments/{appointment_id}/reschedule")
def reschedule_appointment(appointment_id: int, data: RescheduleRequest):
    with lock:
        if not hospital.reschedule_appointment(
            appointment_id, data.new_date, data.new_time
        ):
            raise HTTPException(
                status_code=400,
                detail="Appointment not found or already cancelled",
            )
        return {"message": "Appointment rescheduled successfully"}


@app.get("/api/queue")
def get_queue():
    # Snapshot the heap without removing patients.
    entries = sorted(hospital.patient_queue.queue)
    return [
        {
            "position": index,
            **patient_dict(patient),
        }
        for index, (_, _, patient) in enumerate(entries, start=1)
    ]


@app.post("/api/queue/next")
def call_next_patient():
    with lock:
        patient = hospital.call_next_patient()
        if patient is None:
            raise HTTPException(status_code=404, detail="Patient queue is empty")
        return patient_dict(patient)


@app.get("/api/reports/daily")
def daily_report(report_date: str):
    appointments = [
        a for a in hospital.appointments if a.date == report_date
    ]
    booked = sum(a.status == "Booked" for a in appointments)
    cancelled = sum(a.status == "Cancelled" for a in appointments)
    return {
        "date": report_date,
        "total": len(appointments),
        "booked": booked,
        "cancelled": cancelled,
        "appointments": [appointment_dict(a) for a in appointments],
    }
