# GES Digital Assessment System

An offline-first digital assessment platform for schools. Teachers record students and grades in a Flutter mobile app, sync pending records with a FastAPI backend, and administrators manage data through a React dashboard.

## What’s in the repo

| Directory | Purpose |
| --- | --- |
| `backend/` | FastAPI API, PostgreSQL models, JWT/RBAC security, synchronization, reporting, and audit logging |
| `admin-dashboard/` | React + TypeScript dashboard for administration, reports, users, students, and submitted grades |
| `teacher-mobile/` | Flutter teacher app with SQLite offline storage and a pending-sync queue |
| `documentation/` | Architecture, security, Nginx HTTPS, and deployment documentation |

## Run the app

Use two terminals: one for the backend and one for the dashboard. On Windows PowerShell, run the dashboard with `npm.cmd` if `npm` is blocked by execution policy.

### 1. Create the database

```powershell
psql -f GES-Digital-Assessment-System/backend/scripts/create_database.sql
```

### 2. Install backend dependencies

From the repository root:

```powershell
python -m pip install -r requirements.txt
```

If you prefer to install directly from the backend folder, you can also run:

```powershell
cd GES-Digital-Assessment-System/backend
python -m pip install -r requirements.txt
```

### 3. Start the backend

Set the local environment variables, then launch FastAPI:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/ges_assessment"
$env:JWT_SECRET_KEY = "replace-with-a-strong-unique-secret"
cd GES-Digital-Assessment-System/backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend should respond at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 4. Start the admin dashboard

In a second terminal:

```powershell
cd GES-Digital-Assessment-System/admin-dashboard
npm install
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

The dashboard should open at [http://127.0.0.1:5173](http://127.0.0.1:5173).

## Mobile app

The Flutter source is in `teacher-mobile/`. After installing Flutter, run:

```powershell
cd GES-Digital-Assessment-System/teacher-mobile
flutter pub get
flutter run
```

## Notes

- The backend exposes the versioned API under `/api/v1`.
- The dashboard talks to `http://localhost:8000/api/v1` by default.
- The report PDF generator uses WeasyPrint at runtime, so the backend can start even if the native PDF libraries are not installed yet.
- Production deployments must run behind the Nginx TLS configuration in [documentation/nginx.conf](documentation/nginx.conf).

See [documentation/system-design.md](documentation/system-design.md) for the target normalized schema, API contract, RBAC matrix, and migration plan.
