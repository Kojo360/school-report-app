"""Teacher-facing student, grade, and enrollment-submission routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BehavioralRecord, Enrollment, Student, SubjectGrade
from app.schemas.teacher import (
    EnrollmentSubmissionResponse,
    GradeCreate,
    GradeResponse,
    StudentCreate,
    StudentResponse,
)
from app.security.jwt import require_teacher
from app.services.audit import log_audit


router = APIRouter(dependencies=[Depends(require_teacher)])


@router.get("/students", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)) -> list[Student]:
    """Return all registered students."""
    return db.query(Student).order_by(Student.full_name).all()


@router.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    current_user: dict[str, str] = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> Student:
    """Register a student."""
    student = Student(**student_data.model_dump())
    db.add(student)
    log_audit(db, current_user["sub"], "CREATE_STUDENT", new_value=student_data.model_dump(mode="json"))
    db.commit()
    db.refresh(student)
    return student


@router.post("/grades", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(
    grade_data: GradeCreate,
    current_user: dict[str, str] = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> SubjectGrade:
    """Record a subject grade for a draft enrollment."""
    enrollment = db.get(Enrollment, grade_data.enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    if enrollment.status == "submitted":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Grades cannot be changed after term submission",
        )

    grade = SubjectGrade(**grade_data.model_dump())
    db.add(grade)
    log_audit(db, current_user["sub"], "CREATE_GRADE", new_value=grade_data.model_dump())
    db.commit()
    db.refresh(grade)
    return grade


@router.get("/grades/student/{id}", response_model=list[GradeResponse])
def get_student_grades(id: int, db: Session = Depends(get_db)) -> list[SubjectGrade]:
    """Return all recorded grades for a student across enrollments."""
    student = db.get(Student, id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return (
        db.query(SubjectGrade)
        .join(Enrollment)
        .filter(Enrollment.student_id == id)
        .order_by(SubjectGrade.id)
        .all()
    )


@router.put("/enrollment/{id}/submit", response_model=EnrollmentSubmissionResponse)
def submit_enrollment(
    id: int,
    current_user: dict[str, str] = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> Enrollment:
    """Move an enrollment from draft to submitted."""
    enrollment = db.get(Enrollment, id)
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    if enrollment.status == "submitted":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Enrollment is already submitted"
        )

    enrollment.status = "submitted"
    log_audit(
        db,
        current_user["sub"],
        "SUBMIT_ENROLLMENT",
        old_value={"status": "draft"},
        new_value={"status": "submitted", "enrollment_id": id},
    )
    db.commit()
    db.refresh(enrollment)
    return enrollment
