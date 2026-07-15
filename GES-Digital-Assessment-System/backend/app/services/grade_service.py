from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.models.grade_entry import GradeEntry
from app.models.subject import Subject
from app.models.teacher import Teacher
from app.services.grading_service import calculate_grade

class GradeService:
    def create_grade(self, db: Session, data, user_id: int):
        teacher = db.query(Teacher).filter_by(user_id=user_id).first()
        if teacher is None: raise PermissionError("Only teacher profiles can enter grades")
        enrollment = db.get(Enrollment, data.enrollment_id)
        if enrollment is None: raise LookupError("Enrollment not found")
        if enrollment.status != "draft": raise PermissionError("Enrollment is locked")
        if not db.get(Subject, data.subject_id): raise LookupError("Subject not found")
        result = calculate_grade(data.cat, data.exam)
        grade = GradeEntry(enrollment_id=data.enrollment_id, subject_id=data.subject_id, teacher_id=teacher.id, raw_cat=data.cat, raw_exam=data.exam, total_score=result["total"], letter_grade=result["grade"], remark=result["remark"])
        db.add(grade); db.commit(); db.refresh(grade); return grade
