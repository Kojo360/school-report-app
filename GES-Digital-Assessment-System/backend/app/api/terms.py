from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_admin
from app.database import get_db
from app.models.academic_year import AcademicYear
from app.models.term import Term
from app.models.user import User
from app.schemas.academic import TermCreate, TermResponse
router = APIRouter(prefix="/terms", tags=["Terms"])
@router.post("", response_model=TermResponse)
def create(data: TermCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    if not db.get(AcademicYear, data.academic_year_id): raise HTTPException(404, "Academic year not found")
    row=Term(**data.model_dump()); db.add(row); db.commit(); db.refresh(row); return row
@router.get("", response_model=list[TermResponse])
def list_all(_: User = Depends(get_current_user), db: Session = Depends(get_db)): return db.query(Term).all()
@router.patch("/{term_id}/open", response_model=TermResponse)
def open_term(term_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    row=db.get(Term,term_id)
    if not row: raise HTTPException(404,"Term not found")
    db.query(Term).update({Term.is_open:False}); row.is_open=True; db.commit(); db.refresh(row); return row
