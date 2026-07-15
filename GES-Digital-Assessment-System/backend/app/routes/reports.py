"""Report-card generation API routes."""

from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import BehavioralRecord, Enrollment, Student, SubjectGrade
from app.reports.generator import generate_report_pdf
from app.security.jwt import require_headmaster
from app.services.audit import log_audit


router = APIRouter(tags=["reports"])


@router.post("/reports/generate/{class}")
def generate_class_reports(
    class_level: str = Path(alias="class"),
    current_user: dict[str, str] = Depends(require_headmaster),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    """Generate submitted report cards for a class as a downloadable ZIP file."""
    enrollments = (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.subject_grades),
            joinedload(Enrollment.behavioral_record),
        )
        .filter(Enrollment.class_level == class_level, Enrollment.status == "submitted")
        .all()
    )
    if not enrollments:
        raise HTTPException(status_code=404, detail="No submitted enrollments found for this class")

    archive = BytesIO()
    with ZipFile(archive, "w", ZIP_DEFLATED) as zip_file:
        for enrollment in enrollments:
            safe_name = "_".join(enrollment.student.full_name.split())
            zip_file.writestr(f"{safe_name}_report_card.pdf", generate_report_pdf(enrollment))
    archive.seek(0)
    log_audit(
        db,
        current_user["sub"],
        "GENERATE_CLASS_REPORTS",
        new_value={"class_level": class_level, "report_count": len(enrollments)},
    )
    db.commit()

    headers = {"Content-Disposition": f'attachment; filename="{class_level}_report_cards.zip"'}
    return StreamingResponse(archive, media_type="application/zip", headers=headers)
