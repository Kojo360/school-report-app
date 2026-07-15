"""Behavioral record database model."""

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BehavioralRecord(Base):
    """Attendance and behaviour assessment for an enrollment."""

    __tablename__ = "behavioral_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    enrollment_id: Mapped[int] = mapped_column(
        ForeignKey("enrollments.id"), nullable=False, unique=True
    )
    days_present: Mapped[int] = mapped_column(Integer, nullable=False)
    conduct: Mapped[str] = mapped_column(String(100), nullable=False)
    attitude: Mapped[str] = mapped_column(String(100), nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    enrollment: Mapped["Enrollment"] = relationship(back_populates="behavioral_record")


# Kept as an alias for the "BehaviorRecord" name in the specification.
BehaviorRecord = BehavioralRecord
