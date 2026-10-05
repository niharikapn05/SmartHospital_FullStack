import axios from "axios";

export const api = axios.create({ baseURL: "http://127.0.0.1:8000" });

export type Doctor = { doctor_id:number; name:string; specialization:string; available:boolean };
export type Patient = { patient_id:number; name:string; age:number; phone:string; emergency:boolean; priority:string };
export type Appointment = { appointment_id:number; patient:Patient; doctor:Doctor; date:string; time:string; status:string };

export const getDoctors = () => api.get<Doctor[]>("/api/doctors").then(r=>r.data);
export const getPatients = () => api.get<Patient[]>("/api/patients").then(r=>r.data);
export const getAppointments = () => api.get<Appointment[]>("/api/appointments").then(r=>r.data);
export const getQueue = () => api.get<Patient[]>("/api/queue").then(r=>r.data);
export const addPatient = (data:Omit<Patient,"patient_id"|"priority">) => api.post<Patient>("/api/patients",data).then(r=>r.data);
export const bookAppointment = (data:{patient_id:number;doctor_id:number;date:string;time:string}) => api.post<Appointment>("/api/appointments",data).then(r=>r.data);
export const cancelAppointment = (id:number) => api.patch(`/api/appointments/${id}/cancel`);
export const rescheduleAppointment = (id:number,data:{new_date:string;new_time:string}) => api.patch(`/api/appointments/${id}/reschedule`,data);
export const callNext = () => api.post<Patient>("/api/queue/next").then(r=>r.data);
export const searchDoctors = (specialization:string) => api.get<Doctor[]>("/api/doctors/search",{params:{specialization}}).then(r=>r.data);
export const dailyReport = (date:string) => api.get(`/api/reports/daily`,{params:{report_date:date}}).then(r=>r.data);
