"""Batch synchronization endpoint for offline teacher devices."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BehavioralRecord, Enrollment, Student, SubjectGrade
from app.schemas.sync import SyncItem, SyncRequest, SyncResponse, SyncResult
from app.security.jwt import require_teacher


router = APIRouter(dependencies=[Depends(require_teacher)], tags=["synchronization"])


@router.post("/sync", response_model=SyncResponse)
def sync(request: SyncRequest, db: Session = Depends(get_db)) -> SyncResponse:
    """Store pending offline student and grade records in PostgreSQL."""
    local_student_ids: dict[int, int] = {}
    results: list[SyncResult] = []

    for item in request.items:
        try:
            with db.begin_nested():
                server_id = _sync_item(item, db, local_student_ids)
            results.append(SyncResult(local_id=item.local_id, sync_status="SYNCED", server_id=server_id))
        except (KeyError, TypeError, ValueError) as error:
            results.append(SyncResult(local_id=item.local_id, sync_status="PENDING", error=str(error)))

    db.commit()
    return SyncResponse(items=results)


def _sync_item(item: SyncItem, db: Session, local_student_ids: dict[int, int]) -> int:
    if item.entity_type == "student":
        student = Student(
            full_name=str(item.payload["full_name"]),
            dob=date.fromisoformat(str(item.payload["dob"])),
            admission_date=date.fromisoformat(str(item.payload["admission_date"])),
        )
        db.add(student)
        db.flush()
        local_student_ids[int(item.payload["id"])] = student.id
        return student.id

    local_student_id = int(item.payload["student_id"])
    student_id = local_student_ids.get(local_student_id, local_student_id)
    enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student_id, Enrollment.status == "draft")
        .order_by(Enrollment.id.desc())
        .first()
    )
    if enrollment is None:
        raise ValueError("No draft enrollment found for this student")

    score = float(item.payload["score"])
    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")
    grade = SubjectGrade(
        enrollment_id=enrollment.id,
        subject_name=str(item.payload["subject"]),
        # Mobile records one final score; storing it in both components keeps
        # calculate_score(CAT, EXAM) equal to that supplied final score.
        raw_class_score=score,
        raw_exam_score=score,
    )
    db.add(grade)
    db.flush()
    return grade.id
