# Production security

Serve the FastAPI application behind Nginx using the included `nginx.conf` and a valid TLS certificate (for example, Let's Encrypt). Keep `JWT_SECRET_KEY` in the production secret store and set it to a strong, unique value.

All domain endpoints require a JWT bearer token. `POST /login` remains public so users can obtain a token; teacher endpoints require the `teacher` role, while report generation requires `headmaster`.

Apply the SQL migrations before deployment, including `002_create_audit_logs.sql`.
