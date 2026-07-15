# GES Digital Assessment System

An offline-first digital assessment platform for schools. Teachers record students and grades in a Flutter mobile app, synchronize pending records with a FastAPI backend, and administrators manage assessment data through a React dashboard.

## Components

| Directory | Purpose |
| --- | --- |
| `backend/` | FastAPI API, PostgreSQL models, JWT/RBAC security, synchronization, reporting, and audit logging |
| `teacher-mobile/` | Flutter teacher app with SQLite offline storage and a pending-sync queue |
| `admin-dashboard/` | React + TypeScript dashboard for administration, reports, users, students, and submitted grades |
| `documentation/` | Architecture, security, Nginx HTTPS, and deployment documentation |

## Architecture

```text
Flutter teacher app ── HTTPS + JWT ──┐
                                    ├── FastAPI backend ── PostgreSQL
React admin dashboard ─ HTTPS + JWT ┘
```

The mobile app stores changes locally as `PENDING` while offline. When connectivity returns, the sync service sends them to `POST /sync`; persisted records become `SYNCED`.

## Backend setup

1. Create the PostgreSQL database:

   ```powershell
   psql -f backend/scripts/create_database.sql
   ```

2. Install Python dependencies:

   ```powershell
   cd backend
   python -m pip install -r requirements.txt
   ```

3. Set production secrets and connection details:

   ```powershell
   $env:DATABASE_URL = "postgresql+psycopg://USER:PASSWORD@HOST:5432/ges_assessment"
   $env:JWT_SECRET_KEY = "replace-with-a-strong-unique-secret"
   ```

4. Apply SQL migrations in `backend/scripts/migrations/`, then run:

   ```powershell
   uvicorn app.main:app --reload
   ```

## Frontend setup

```powershell
cd admin-dashboard
npm install
npm run dev
```

The Flutter source is in `teacher-mobile/`. After installing Flutter, run `flutter pub get` and `flutter run` from that directory.

## Security

Domain API endpoints use JWT bearer tokens and role-based access control. Teachers manage their assigned draft grades; headmasters approve reports; administrators manage system-wide data. Production deployments must run behind the Nginx TLS configuration in [documentation/nginx.conf](documentation/nginx.conf).

See [System Design](documentation/system-design.md) for the target normalized database schema, API contract, RBAC matrix, and data migration plan.
