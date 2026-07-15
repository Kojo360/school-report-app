from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.student import Gender, StudentStatus

class StudentCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    gender: Gender
    date_of_birth: date
    admission_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.date_of_birth > date.today(): raise ValueError("Date of birth cannot be in the future")
        if self.admission_date < self.date_of_birth: raise ValueError("Admission date cannot be before date of birth")
        return self

class StudentUpdate(StudentCreate):
    pass

class StudentResponse(StudentCreate):
    id: int
    student_number: str
    status: StudentStatus
    model_config = ConfigDict(from_attributes=True)

class StudentPage(BaseModel):
    page: int
    size: int
    total: int
    items: list[StudentResponse]
