from datetime import date
from sqlalchemy.orm import Session
from app.models.student import Student, StudentStatus
from app.repositories.student_repository import StudentRepository

class StudentService:
    def __init__(self): self.repository = StudentRepository()
    def create_student(self, db: Session, data):
        student = Student(student_number="PENDING", **data.model_dump())
        db.add(student); db.flush()
        student.student_number = f"GES-{date.today().year}-{student.id:04d}"
        db.commit(); db.refresh(student); return student
    def update_student(self, db: Session, student_id: int, data):
        student = self.require(db, student_id)
        for key, value in data.model_dump().items(): setattr(student, key, value)
        db.commit(); db.refresh(student); return student
    def archive_student(self, db: Session, student_id: int):
        student = self.require(db, student_id); student.status = StudentStatus.TRANSFERRED
        db.commit(); db.refresh(student); return student
    def require(self, db: Session, student_id: int):
        student = self.repository.get_by_id(db, student_id)
        if student is None: raise LookupError("Student not found")
        return student
