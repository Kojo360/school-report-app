# GES Digital Assessment System — Architecture Baseline

## System architecture

```text
Flutter teacher app ── HTTPS + JWT ──┐
                                    │
React admin dashboard ─ HTTPS + JWT ├── FastAPI backend ── PostgreSQL
                                    │       ├─ Authentication / RBAC
                                    │       ├─ Student management
                                    │       ├─ Grade management
                                    │       ├─ Report and PDF engine
                                    │       ├─ Offline synchronization
                                    │       └─ Audit logging
                                    │
Flutter SQLite queue ───────────────┘
```

The Flutter app is offline-first: it writes changes to SQLite and labels queued records `PENDING`. When connectivity returns, it sends the queue to `POST /sync`; successfully persisted records become `SYNCED`.

## Backend layers

The production backend uses this dependency direction:

```text
api → services → repositories → models/database
```

| Layer | Responsibility |
| --- | --- |
| `api/` | HTTP routes, validation, authentication dependencies, response codes |
| `services/` | workflows, grading rules, report generation, synchronization |
| `repositories/` | database queries and persistence operations |
| `models/` | SQLAlchemy relational models |
| `schemas/` | Pydantic request and response contracts |
| `security/` | JWT, password hashing, role enforcement |
| `reports/` | HTML templates and PDF generation |
| `utils/` | shared non-domain helpers |

Target application layout:

```text
backend/app/
├── api/                 # auth, users, students, classes, subjects, grades, reports, sync
├── models/
├── schemas/
├── services/
├── repositories/
├── security/
├── utils/
├── reports/
├── database/
└── main.py
```

## Production data model

### Core identity

| Table | Important fields | Relationships |
| --- | --- | --- |
| `roles` | `id`, `name` | one role has many users |
| `users` | `id`, `username`, `email`, `password_hash`, `role_id`, `is_active` | belongs to a role; optionally has one teacher profile |
| `teachers` | `id`, `user_id`, `full_name`, `phone` | belongs to a user; teaches classes and records grades |

Role names are `teacher`, `headmaster`, and `administrator`.

### Academic structure

| Table | Important fields | Relationships |
| --- | --- | --- |
| `academic_years` | `id`, `name`, `starts_on`, `ends_on`, `is_active` | has terms |
| `terms` | `id`, `academic_year_id`, `name`, `starts_on`, `ends_on` | belongs to an academic year |
| `classes` | `id`, `name`, `teacher_id` | assigned to a teacher; has enrollments |
| `subjects` | `id`, `code`, `name` | referenced by grade entries |

### Student assessment

| Table | Important fields | Relationships |
| --- | --- | --- |
| `students` | `id`, `student_number`, `full_name`, `gender`, `date_of_birth`, `admission_date` | has enrollments |
| `enrollments` | `id`, `student_id`, `class_id`, `term_id`, `academic_year_id`, `status` | has grades, attendance, and one behaviour record |
| `grade_entries` | `id`, `enrollment_id`, `subject_id`, `teacher_id`, `raw_cat`, `raw_exam`, `total`, `grade`, `remark` | belongs to enrollment, subject, and teacher |
| `behavior_records` | `id`, `enrollment_id`, `conduct`, `attitude`, `remarks` | one per enrollment |
| `attendance` | `id`, `enrollment_id`, `days_present`, `days_absent` | belongs to enrollment |
| `report_cards` | `id`, `enrollment_id`, `status`, `file_path`, `generated_at`, `approved_by` | one per published enrollment report |

### Operations and traceability

| Table | Important fields |
| --- | --- |
| `audit_logs` | `id`, `user`, `action`, `timestamp`, `old_value`, `new_value` |
| `sync_logs` | `id`, `user_id`, `device_id`, `entity_type`, `local_id`, `server_id`, `status`, `error`, `synced_at` |

`grade_entries.subject_id` is the canonical subject reference. A grade must never duplicate a subject name; renaming a subject is therefore a single update to `subjects.name`.

## Key relationships

```text
Role 1 ── * User 1 ── 0..1 Teacher
Teacher 1 ── * Class
Student 1 ── * Enrollment * ── 1 Class
Enrollment 1 ── * GradeEntry * ── 1 Subject
Enrollment 1 ── * Attendance
Enrollment 1 ── 0..1 BehaviorRecord
Enrollment 1 ── 0..1 ReportCard
Teacher 1 ── * GradeEntry
AcademicYear 1 ── * Term 1 ── * Enrollment
```

## API contract

All endpoints except `POST /auth/login` require `Authorization: Bearer <JWT>`. The canonical API version is `/api/v1`.

| Domain | Endpoint |
| --- | --- |
| Authentication | `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, `POST /api/v1/auth/refresh` |
| Users | `GET/POST /api/v1/users`, `PUT/DELETE /api/v1/users/{id}` |
| Students | `GET/POST /api/v1/students`, `GET/PUT/DELETE /api/v1/students/{id}` |
| Classes | `GET/POST /api/v1/classes` |
| Subjects | `GET/POST /api/v1/subjects` |
| Grades | `POST /api/v1/grades`, `PUT /api/v1/grades/{id}`, `GET /api/v1/grades/student/{id}`, `GET /api/v1/grades/class/{class_id}` |
| Reports | `POST /api/v1/reports/generate`, `GET /api/v1/reports/download/{id}` |
| Sync | `POST /api/v1/sync`, `GET /api/v1/sync/status` |

The current unversioned prototype routes remain temporary compatibility endpoints. New mobile and dashboard work must use the versioned contract above.

## Role-based access control

| Capability | Teacher | Headmaster | Administrator |
| --- | :---: | :---: | :---: |
| View assigned students/classes | Yes | Yes | Yes |
| Create and edit draft grades | Yes | No | Yes |
| Submit grades | Yes | No | Yes |
| Approve submitted grades | No | Yes | Yes |
| Generate/publish reports | No | Yes | Yes |
| Manage users, roles, classes, subjects | No | No | Yes |

The authorization service must enforce these rules server-side; hiding a dashboard button is not authorization.

## Student workflow and state transitions

```text
Create student → enroll in class/year/term → teacher enters draft grades
→ teacher submits enrollment (locked) → headmaster approves
→ report card is generated and published
```

Recommended enrollment states: `draft`, `submitted`, `approved`, `published`.

Only a draft enrollment is editable by a teacher. Approval and publication are irreversible operational actions and must create audit-log entries.

## Migration from the prototype

1. Introduce the new normalized tables and repository layer without deleting current tables.
2. Backfill `subjects` from distinct legacy `subject_name` values.
3. Create `grade_entries` from legacy `subject_grades`, assigning the appropriate subject and teacher.
4. Backfill academic years, terms, classes, and normalized enrollments.
5. Switch API clients to `/api/v1` and the new schema.
6. Verify counts and reports, then retire legacy models and routes in a scheduled breaking release.

This migration avoids losing previously entered student and grade data.
