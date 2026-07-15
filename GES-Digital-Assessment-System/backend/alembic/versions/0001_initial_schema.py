"""Initial normalized assessment schema."""
from alembic import op
from app.database.base import Base
import app.models.role, app.models.user, app.models.teacher, app.models.student
import app.models.class_model, app.models.subject, app.models.academic_year, app.models.term
import app.models.enrollment, app.models.grade_entry, app.models.attendance
import app.models.behavior_record, app.models.report_card, app.models.audit_log, app.models.sync_log

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    Base.metadata.create_all(bind=op.get_bind())

def downgrade():
    Base.metadata.drop_all(bind=op.get_bind())
