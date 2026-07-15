from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class GradeCreate(BaseModel):
    enrollment_id: int
    subject_id: int
    cat: float = Field(ge=0, le=100)
    exam: float = Field(ge=0, le=100)
class GradeResponse(BaseModel):
    id: int; enrollment_id: int; subject_id: int; teacher_id: int; raw_cat: float; raw_exam: float; total_score: float; letter_grade: str; remark: str; submitted: bool; created_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
