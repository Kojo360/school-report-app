from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Attendance(Base):
    __tablename__ = "attendance"; __table_args__ = (UniqueConstraint("enrollment_id"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollments.id"), nullable=False)
    days_present: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    days_absent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    times_late: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
