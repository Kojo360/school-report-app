from pydantic import BaseModel, ConfigDict, Field

class AcademicYearCreate(BaseModel): year_name: str = Field(pattern=r"^\d{4}/\d{4}$")
class AcademicYearUpdate(BaseModel): year_name: str | None = Field(default=None, pattern=r"^\d{4}/\d{4}$"); is_current: bool | None = None
class AcademicYearResponse(BaseModel):
    id: int; year_name: str; is_current: bool
    model_config = ConfigDict(from_attributes=True)
class TermCreate(BaseModel): name: str = Field(min_length=1, max_length=20); academic_year_id: int
class TermResponse(TermCreate):
    id: int; is_open: bool
    model_config = ConfigDict(from_attributes=True)
class SubjectCreate(BaseModel): code: str = Field(min_length=2, max_length=10); name: str = Field(min_length=2, max_length=100)
class SubjectResponse(SubjectCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
class ClassCreate(BaseModel): name: str = Field(min_length=2, max_length=50)
class ClassResponse(ClassCreate):
    id: int; teacher_id: int | None
    model_config = ConfigDict(from_attributes=True)
