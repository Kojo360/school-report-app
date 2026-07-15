"""Enrollment database model."""

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Enrollment(Base):
    """A student's placement in a class for an academic term."""

    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "academic_year", "term", name="uq_student_term"),
        CheckConstraint("status IN ('draft', 'submitted')", name="ck_enrollments_status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    term: Mapped[str] = mapped_column(String(30), nullable=False)
    class_level: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    subject_grades: Mapped[list["SubjectGrade"]] = relationship(
        back_populates="enrollment", cascade="all, delete-orphan"
    )
    behavioral_record: Mapped["BehavioralRecord | None"] = relationship(
        back_populates="enrollment", cascade="all, delete-orphan", uselist=False
    )
