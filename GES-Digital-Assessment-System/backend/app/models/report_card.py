from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class ReportCard(Base):
    __tablename__ = "report_cards"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollments.id"), unique=True, nullable=False)
    overall_average: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    position: Mapped[int | None] = mapped_column(Integer)
    teacher_remark: Mapped[str | None] = mapped_column(String(500))
    headmaster_remark: Mapped[str | None] = mapped_column(String(500))
    pdf_path: Mapped[str | None] = mapped_column(String(500))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
