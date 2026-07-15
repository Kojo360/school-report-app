from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class GradeEntry(Base):
    __tablename__ = "grade_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollments.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    raw_cat: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    raw_exam: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    total_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    letter_grade: Mapped[str] = mapped_column(String(2), nullable=False)
    remark: Mapped[str] = mapped_column(String(100), nullable=False)
    submitted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
