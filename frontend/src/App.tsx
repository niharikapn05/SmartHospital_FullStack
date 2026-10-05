import { useEffect, useMemo, useState } from "react";
import { Activity, CalendarDays, CheckCircle2, ChevronRight, Clock3, HeartPulse, Hospital, LayoutDashboard, LogOut, Search, Stethoscope, UserPlus, Users, XCircle } from "lucide-react";
import { addPatient, api, Appointment, bookAppointment, callNext, cancelAppointment, dailyReport, Doctor, getAppointments, getDoctors, getPatients, getQueue, Patient, rescheduleAppointment, searchDoctors } from "./api";
import "./styles.css";

type Tab = "dashboard"|"patients"|"doctors"|"appointments"|"queue"|"report";

function App(){
  const [tab,setTab]=useState<Tab>("dashboard");
  const [doctors,setDoctors]=useState<Doctor[]>([]);
  const [patients,setPatients]=useState<Patient[]>([]);
  const [appointments,setAppointments]=useState<Appointment[]>([]);
  const [queue,setQueue]=useState<Patient[]>([]);
  const [error,setError]=useState("");
  const [toast,setToast]=useState("");
  const [loading,setLoading]=useState(true);

  const refresh=async()=>{
    setLoading(true); setError("");
    try{
      const [d,p,a,q]=await Promise.all([getDoctors(),getPatients(),getAppointments(),getQueue()]);
      setDoctors(d); setPatients(p); setAppointments(a); setQueue(q);
    }catch(e:any){ setError(e?.response?.data?.detail || "Cannot connect to backend. Start the FastAPI server."); }
    finally{setLoading(false)}
  };
  useEffect(()=>{refresh()},[]);
  const notify=(m:string)=>{setToast(m);setTimeout(()=>setToast(""),3000)}
  const run=async(fn:()=>Promise<any>,msg:string)=>{try{await fn();await refresh();notify(msg)}catch(e:any){setError(e?.response?.data?.detail||"Operation failed")}}

  const stats=[
    ["Patients",patients.length,Users],
    ["Doctors",doctors.length,Stethoscope],
    ["Appointments",appointments.length,CalendarDays],
    ["Queue",queue.length,Clock3]
  ];
  const today = new Date().toISOString().slice(0,10);
  const todayAppointments=appointments.filter(a=>a.date===today);
  const activeAppointments=appointments.filter(a=>a.status==="Booked");

  return <div className="app">
    <aside className="sidebar">
      <div className="brand"><div className="brand-icon"><HeartPulse/></div><div><b>SmartCare</b><span>Hospital System</span></div></div>
      <div className="nav-label">MAIN MENU</div>
      <Nav icon={LayoutDashboard} label="Dashboard" active={tab==="dashboard"} onClick={()=>setTab("dashboard")}/>
      <Nav icon={Users} label="Patients" active={tab==="patients"} onClick={()=>setTab("patients")}/>
      <Nav icon={Stethoscope} label="Doctors" active={tab==="doctors"} onClick={()=>setTab("doctors")}/>
      <Nav icon={CalendarDays} label="Appointments" active={tab==="appointments"} onClick={()=>setTab("appointments")}/>
      <Nav icon={Clock3} label="Patient Queue" active={tab==="queue"} onClick={()=>setTab("queue")}/>
      <Nav icon={Activity} label="Daily Report" active={tab==="report"} onClick={()=>setTab("report")}/>
      <div className="sidebar-bottom"><div className="mini-card"><span>System Status</span><b><i/> API Connected</b></div><button className="logout" onClick={()=>notify("This demo has no authentication configured.")}><LogOut size={17}/> Sign out</button></div>
    </aside>
    <main>
      <header><div><div className="crumb">SMART HOSPITAL / {tab.toUpperCase()}</div><h1>{tab==="dashboard"?"Good morning, Doctor":title(tab)}</h1></div><div className="header-right"><span className="date">{new Date().toLocaleDateString(undefined,{weekday:"short",month:"short",day:"numeric"})}</span><div className="avatar">SH</div></div></header>
      {error&&<div className="error"><XCircle size={18}/>{error}<button onClick={refresh}>Retry</button></div>}
      {toast&&<div className="toast"><CheckCircle2 size={18}/>{toast}</div>}
      {loading&&<div className="loading">Loading hospital data…</div>}
      {!loading&&tab==="dashboard"&&<Dashboard stats={stats} today={todayAppointments} queue={queue} onBook={()=>setTab("appointments")} />}
      {!loading&&tab==="patients"&&<Patients patients={patients} onAdd={async d=>run(()=>addPatient(d),"Patient registered successfully")}/>}
      {!loading&&tab==="doctors"&&<Doctors doctors={doctors}/>}
      {!loading&&tab==="appointments"&&<Appointments patients={patients} doctors={doctors} appointments={appointments} onBook={d=>run(()=>bookAppointment(d),"Appointment booked successfully")} onCancel={id=>run(()=>cancelAppointment(id),"Appointment cancelled")} onReschedule={(id,d)=>run(()=>rescheduleAppointment(id,d),"Appointment rescheduled")}/>}
      {!loading&&tab==="queue"&&<Queue queue={queue} onNext={async()=>{try{const p=await callNext();await refresh();notify(`${p.name} has been called.`)}catch(e:any){setError(e?.response?.data?.detail||"Queue is empty")}}}/>}
      {!loading&&tab==="report"&&<Report appointments={appointments}/>}
    </main>
  </div>
}

function title(t:Tab){return ({dashboard:"Dashboard",patients:"Patient Management",doctors:"Doctor Directory",appointments:"Appointment Management",queue:"Patient Queue",report:"Daily Appointment Report"} as any)[t]}
function Nav({icon:Icon,label,active,onClick}:any){return <button className={"nav "+(active?"active":"")} onClick={onClick}><Icon size={19}/>{label}<ChevronRight className="nav-arrow" size={15}/></button>}

function Dashboard({stats,today,queue,onBook}:any){
 return <><section className="hero"><div><div className="eyebrow">CARE AT A GLANCE</div><h2>Hospital operations, simplified.</h2><p>Manage patients, doctors, appointments and priority queues from one place.</p><button className="primary" onClick={onBook}><CalendarDays size={17}/> Book an appointment</button></div><div className="hero-art"><Hospital size={74}/><span>24/7<br/><small>Patient Care</small></span></div></section>
 <div className="stats">{stats.map(([name,value,Icon]:any)=><div className="stat" key={name}><div className="stat-icon"><Icon size={20}/></div><div><span>{name}</span><strong>{value}</strong></div></div>)}</div>
 <div className="grid-two"><section className="panel"><div className="panel-head"><div><h3>Today’s appointments</h3><p>Scheduled for today</p></div><span className="badge">{today.length} total</span></div>{today.length?<Table appointments={today}/>:<Empty text="No appointments scheduled for today."/>}</section>
 <section className="panel"><div className="panel-head"><div><h3>Priority queue</h3><p>Emergency patients are called first</p></div><span className="badge warning">{queue.length} waiting</span></div>{queue.slice(0,5).map((p:Patient)=><div className="queue-row" key={p.patient_id}><div className={"priority "+p.priority.toLowerCase()}>{p.priority==="EMERGENCY"?"E":"N"}</div><div><b>{p.name}</b><span>Patient #{p.patient_id} · {p.age} yrs</span></div><strong>{p.priority}</strong></div>)}{!queue.length&&<Empty text="Patient queue is empty."/>}</section></div></>
}
function Empty({text}:{text:string}){return <div className="empty"><Activity size={25}/><span>{text}</span></div>}
function Table({appointments}:{appointments:Appointment[]}){return <div className="table-wrap"><table><thead><tr><th>Patient</th><th>Doctor</th><th>Date</th><th>Time</th><th>Status</th></tr></thead><tbody>{appointments.map(a=><tr key={a.appointment_id}><td><b>{a.patient.name}</b><small>#{a.patient.patient_id}</small></td><td>{a.doctor.name}<small>{a.doctor.specialization}</small></td><td>{a.date}</td><td>{a.time}</td><td><span className={"status "+a.status.toLowerCase()}>{a.status}</span></td></tr>)}</tbody></table></div>}

function Patients({patients,onAdd}:{patients:Patient[],onAdd:(d:any)=>Promise<any>}){const [open,setOpen]=useState(false);return <><SectionHead title="Patients" sub={`${patients.length} registered patients`} action={<button className="primary" onClick={()=>setOpen(true)}><UserPlus size={17}/> Register patient</button>}/><section className="panel"><div className="table-wrap"><table><thead><tr><th>ID</th><th>Patient</th><th>Age</th><th>Phone</th><th>Priority</th></tr></thead><tbody>{patients.map(p=><tr key={p.patient_id}><td>#{p.patient_id}</td><td><b>{p.name}</b></td><td>{p.age}</td><td>{p.phone}</td><td><span className={"priority-pill "+p.priority.toLowerCase()}>{p.priority}</span></td></tr>)}</tbody></table></div>{!patients.length&&<Empty text="No patients registered yet."/>}</section>{open&&<PatientModal onClose={()=>setOpen(false)} onSave={async d=>{await onAdd(d);setOpen(false)}}/>}</>}
function SectionHead({title,sub,action}:any){return <div className="section-head"><div><h2>{title}</h2><p>{sub}</p></div>{action}</div>}
function PatientModal({onClose,onSave}:any){const [f,setF]=useState({name:"",age:"",phone:"",emergency:false});return <Modal title="Register Patient" onClose={onClose}><form onSubmit={e=>{e.preventDefault();onSave({...f,age:Number(f.age)})}}><label>Full name<input required value={f.name} onChange={e=>setF({...f,name:e.target.value})}/></label><div className="form-row"><label>Age<input required type="number" min="0" value={f.age} onChange={e=>setF({...f,age:e.target.value})}/></label><label>Phone<input required value={f.phone} onChange={e=>setF({...f,phone:e.target.value})}/></label></div><label className="check"><input type="checkbox" checked={f.emergency} onChange={e=>setF({...f,emergency:e.target.checked})}/> Emergency case</label><button className="primary wide">Register patient</button></form></Modal>}
function Modal({title,children,onClose}:any){return <div className="overlay"><div className="modal"><div className="modal-head"><h3>{title}</h3><button onClick={onClose}><XCircle/></button></div>{children}</div></div>}

function Doctors({doctors}:{doctors:Doctor[]}){const [q,setQ]=useState("");const filtered=useMemo(()=>q?doctors.filter(d=>d.name.toLowerCase().includes(q.toLowerCase())||d.specialization.toLowerCase().includes(q.toLowerCase())):doctors,[doctors,q]);return <><SectionHead title="Doctor Directory" sub={`${doctors.length} doctors available`}/><div className="search"><Search size={18}/><input placeholder="Search by doctor or specialization…" value={q} onChange={e=>setQ(e.target.value)}/></div><div className="doctor-grid">{filtered.map(d=><div className="doctor-card" key={d.doctor_id}><div className="doc-avatar">{d.name.replace("Dr. ","").split(" ").map(x=>x[0]).join("").slice(0,2)}</div><div><h3>{d.name}</h3><p>{d.specialization}</p><span className="available"><i/> {d.available?"Available":"Unavailable"}</span></div><span className="doc-id">#{d.doctor_id}</span></div>)}</div></>}
function Appointments({patients,doctors,appointments,onBook,onCancel,onReschedule}:any){const [mode,setMode]=useState<"book"|"reschedule">("book");const [form,setForm]=useState({patient_id:"",doctor_id:"",date:new Date().toISOString().slice(0,10),time:"10:00 AM"});const [rid,setRid]=useState("");const submit=(e:any)=>{e.preventDefault();if(mode==="book")onBook({...form,patient_id:Number(form.patient_id),doctor_id:Number(form.doctor_id)});else onReschedule(Number(rid),{new_date:form.date,new_time:form.time})};return <><SectionHead title="Appointments" sub={`${appointments.filter((a:Appointment)=>a.status==="Booked").length} active appointments`} action={<div className="seg"><button className={mode==="book"?"selected":""} onClick={()=>setMode("book")}>Book</button><button className={mode==="reschedule"?"selected":""} onClick={()=>setMode("reschedule")}>Reschedule</button></div>}/><section className="panel form-panel"><form onSubmit={submit}>{mode==="book"?<div className="form-row"><label>Patient<select required value={form.patient_id} onChange={e=>setForm({...form,patient_id:e.target.value})}><option value="">Select patient</option>{patients.map((p:Patient)=><option key={p.patient_id} value={p.patient_id}>#{p.patient_id} — {p.name}</option>)}</select></label><label>Doctor<select required value={form.doctor_id} onChange={e=>setForm({...form,doctor_id:e.target.value})}><option value="">Select doctor</option>{doctors.map((d:Doctor)=><option key={d.doctor_id} value={d.doctor_id}>{d.name} — {d.specialization}</option>)}</select></label></div>:<label>Appointment ID<select required value={rid} onChange={e=>setRid(e.target.value)}><option value="">Select appointment</option>{appointments.filter((a:Appointment)=>a.status==="Booked").map((a:Appointment)=><option key={a.appointment_id} value={a.appointment_id}>#{a.appointment_id} — {a.patient.name} with {a.doctor.name}</option>)}</select></label>}<div className="form-row"><label>Date<input type="date" required value={form.date} onChange={e=>setForm({...form,date:e.target.value})}/></label><label>Time<input required value={form.time} onChange={e=>setForm({...form,time:e.target.value})}/></label></div><button className="primary">{mode==="book"?"Book appointment":"Save new schedule"}</button></form></section><section className="panel"><div className="panel-head"><div><h3>Appointment list</h3><p>Manage existing bookings</p></div></div><div className="table-wrap"><table><thead><tr><th>ID</th><th>Patient</th><th>Doctor</th><th>Date / Time</th><th>Status</th><th>Action</th></tr></thead><tbody>{appointments.map((a:Appointment)=><tr key={a.appointment_id}><td>#{a.appointment_id}</td><td><b>{a.patient.name}</b></td><td>{a.doctor.name}</td><td>{a.date}<small>{a.time}</small></td><td><span className={"status "+a.status.toLowerCase()}>{a.status}</span></td><td>{a.status==="Booked"&&<button className="danger-btn" onClick={()=>onCancel(a.appointment_id)}>Cancel</button>}</td></tr>)}</tbody></table></div>{!appointments.length&&<Empty text="No appointments yet."/>}</section></>}
function Queue({queue,onNext}:{queue:Patient[],onNext:()=>void}){return <><SectionHead title="Patient Queue" sub="Priority-based queue using a heap data structure" action={<button className="primary" disabled={!queue.length} onClick={onNext}><ChevronRight size={17}/> Call next patient</button>}/><div className="queue-hero"><div><span>WAITING PATIENTS</span><strong>{queue.length}</strong><p>Emergency cases are prioritized automatically.</p></div><div className="queue-symbol">∞</div></div><section className="panel"><div className="panel-head"><div><h3>Current queue</h3><p>Order determined by patient priority and registration time</p></div></div>{queue.map((p,i)=><div className="big-queue" key={p.patient_id}><span className="position">{i+1}</span><div className={"priority "+p.priority.toLowerCase()}>{p.priority==="EMERGENCY"?"E":"N"}</div><div className="q-main"><b>{p.name}</b><span>Patient #{p.patient_id} · {p.age} years · {p.phone}</span></div><span className={"priority-pill "+p.priority.toLowerCase()}>{p.priority}</span></div>)}{!queue.length&&<Empty text="Queue is empty."/>}</section></>}
function Report({appointments}:{appointments:Appointment[]}){const [date,setDate]=useState(new Date().toISOString().slice(0,10));const [report,setReport]=useState<any>(null);useEffect(()=>{dailyReport(date).then(setReport).catch(()=>{})},[date,appointments.length]);return <><SectionHead title="Daily Report" sub="Appointment activity by date"/><section className="panel report-top"><label>Report date<input type="date" value={date} onChange={e=>setDate(e.target.value)}/></label></section>{report&&<><div className="stats"><div className="stat"><div className="stat-icon"><CalendarDays/></div><div><span>Total</span><strong>{report.total}</strong></div></div><div className="stat"><div className="stat-icon"><CheckCircle2/></div><div><span>Booked</span><strong>{report.booked}</strong></div></div><div className="stat"><div className="stat-icon"><XCircle/></div><div><span>Cancelled</span><strong>{report.cancelled}</strong></div></div></div><section className="panel"><Table appointments={report.appointments}/></section></>}</>}
export default App;
