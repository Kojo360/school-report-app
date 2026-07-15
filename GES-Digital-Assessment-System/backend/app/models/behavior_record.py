from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class BehaviorRecord(Base):
    __tablename__ = "behavior_records"; __table_args__ = (UniqueConstraint("enrollment_id"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollments.id"), nullable=False)
    conduct: Mapped[str] = mapped_column(String(100), nullable=False)
    attitude: Mapped[str] = mapped_column(String(100), nullable=False)
    interest: Mapped[str] = mapped_column(String(100), nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text)
