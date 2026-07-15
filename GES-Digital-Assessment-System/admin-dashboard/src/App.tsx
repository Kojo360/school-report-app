import type { ReactNode } from 'react'
import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import './App.css'

const links = [
  ['/', 'Dashboard'],
  ['/students', 'Students'],
  ['/submitted-grades', 'Submitted Grades'],
  ['/reports', 'Reports'],
  ['/users', 'Users'],
]

function Layout() {
  return (
    <div className="app-shell">
      <aside>
        <h1>GES Assessments</h1>
        <nav>{links.map(([to, label]) => <NavLink key={to} to={to} end={to === '/'}>{label}</NavLink>)}</nav>
        <NavLink className="logout" to="/login">Sign out</NavLink>
      </aside>
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/students" element={<Students />} />
          <Route path="/submitted-grades" element={<SubmittedGrades />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/users" element={<Users />} />
        </Routes>
      </main>
    </div>
  )
}

function Page({ title, children }: { title: string; children: ReactNode }) {
  return <section><h2>{title}</h2>{children}</section>
}

function Dashboard() {
  return <Page title="Dashboard"><div className="cards"><Metric label="Students" value="0" /><Metric label="Submitted terms" value="0" /><Metric label="Pending sync" value="0" /></div></Page>
}
function Metric({ label, value }: { label: string; value: string }) { return <article className="card"><span>{label}</span><strong>{value}</strong></article> }
function Students() { return <Page title="Students"><Empty text="No students loaded yet." /></Page> }
function SubmittedGrades() { return <Page title="Submitted Grades"><Empty text="No submitted grades yet." /></Page> }
function Reports() { return <Page title="Reports"><p>Generate and download term assessment reports here.</p></Page> }
function Users() { return <Page title="Users"><Empty text="No users loaded yet." /></Page> }
function Empty({ text }: { text: string }) { return <div className="empty">{text}</div> }

function Login() {
  return <div className="login"><form><h1>GES Admin</h1><p>Sign in to manage assessments.</p><label>Username<input autoComplete="username" /></label><label>Password<input type="password" autoComplete="current-password" /></label><NavLink className="button" to="/">Sign in</NavLink></form></div>
}

export default function App() {
  return <Routes><Route path="/login" element={<Login />} /><Route path="/*" element={<Layout />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes>
}
