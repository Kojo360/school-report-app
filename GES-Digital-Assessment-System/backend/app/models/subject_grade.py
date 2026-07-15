"""Subject-grade database model."""

from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SubjectGrade(Base):
    """A class and examination score for one subject enrollment."""

    __tablename__ = "subject_grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollments.id"), nullable=False)
    subject_name: Mapped[str] = mapped_column(String(100), nullable=False)
    raw_class_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    raw_exam_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)

    enrollment: Mapped["Enrollment"] = relationship(back_populates="subject_grades")
