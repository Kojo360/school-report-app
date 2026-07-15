from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.student import Student

class StudentRepository:
    def get_by_id(self, db: Session, student_id: int): return db.get(Student, student_id)
    def get_page(self, db: Session, page: int, size: int, name: str | None = None, student_number: str | None = None, gender=None):
        query = db.query(Student)
        if name: query = query.filter(Student.full_name.ilike(f"%{name}%"))
        if student_number: query = query.filter(Student.student_number.ilike(f"%{student_number}%"))
        if gender: query = query.filter(Student.gender == gender)
        return query.order_by(Student.full_name).offset((page - 1) * size).limit(size).all(), query.with_entities(func.count()).scalar()
