from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import require_teacher
from app.database import get_db
from app.models.user import User
from app.schemas.grade import GradeCreate, GradeResponse
from app.services.grade_service import GradeService
router = APIRouter(prefix="/grades", tags=["Grades"])
service = GradeService()
@router.post("", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(data: GradeCreate, user: User = Depends(require_teacher), db: Session = Depends(get_db)):
    try: return service.create_grade(db, data, user.id)
    except LookupError as error: raise HTTPException(404, str(error)) from error
    except (PermissionError, ValueError) as error: raise HTTPException(403, str(error)) from error
