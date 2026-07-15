"""Schemas for teacher-facing student and grade operations."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    dob: date
    admission_date: date


class StudentResponse(StudentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GradeCreate(BaseModel):
    enrollment_id: int
    subject_name: str = Field(min_length=1, max_length=100)
    raw_class_score: float = Field(ge=0, le=100)
    raw_exam_score: float = Field(ge=0, le=100)


class GradeResponse(GradeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EnrollmentSubmissionResponse(BaseModel):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
