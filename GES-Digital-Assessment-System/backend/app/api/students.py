from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_headmaster
from app.database.dependency import get_db
from app.models.student import Gender
from app.models.user import User
from app.schemas.student import StudentCreate, StudentPage, StudentResponse, StudentUpdate
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])
service = StudentService()

@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, _: User = Depends(require_headmaster), db: Session = Depends(get_db)):
    return service.create_student(db, data)

@router.get("", response_model=StudentPage)
def get_students(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), name: str | None = None, student_number: str | None = None, gender: Gender | None = None, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items, total = service.repository.get_page(db, page, size, name, student_number, gender)
    return {"page": page, "size": size, "total": total, "items": items}

@router.get("/search", response_model=StudentPage)
def search_students(name: str, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items, total = service.repository.get_page(db, 1, 20, name=name)
    return {"page": 1, "size": 20, "total": total, "items": items}

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try: return service.require(db, student_id)
    except LookupError as error: raise HTTPException(404, str(error)) from error

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentUpdate, _: User = Depends(require_headmaster), db: Session = Depends(get_db)):
    try: return service.update_student(db, student_id, data)
    except LookupError as error: raise HTTPException(404, str(error)) from error

@router.patch("/{student_id}/archive", response_model=StudentResponse)
def archive_student(student_id: int, _: User = Depends(require_headmaster), db: Session = Depends(get_db)):
    try: return service.archive_student(db, student_id)
    except LookupError as error: raise HTTPException(404, str(error)) from error
