from alembic import context
from app.database import DATABASE_URL
from app.database.base import Base
import app.models.role, app.models.user, app.models.teacher, app.models.student
import app.models.class_model, app.models.subject, app.models.academic_year, app.models.term
import app.models.enrollment, app.models.grade_entry, app.models.attendance
import app.models.behavior_record, app.models.report_card, app.models.audit_log, app.models.sync_log

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction(): context.run_migrations()

def run_migrations_online():
    from sqlalchemy import engine_from_config, pool
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction(): context.run_migrations()

if context.is_offline_mode(): run_migrations_offline()
else: run_migrations_online()
