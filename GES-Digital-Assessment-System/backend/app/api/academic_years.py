from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import require_admin, get_current_user
from app.database import get_db
from app.models.academic_year import AcademicYear
from app.models.user import User
from app.schemas.academic import AcademicYearCreate, AcademicYearResponse, AcademicYearUpdate
router = APIRouter(prefix="/academic-years", tags=["Academic Years"])
@router.post("", response_model=AcademicYearResponse)
def create(data: AcademicYearCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    if db.query(AcademicYear).filter_by(year_name=data.year_name).first(): raise HTTPException(409, "Academic year already exists")
    row = AcademicYear(**data.model_dump()); db.add(row); db.commit(); db.refresh(row); return row
@router.get("", response_model=list[AcademicYearResponse])
def list_all(_: User = Depends(get_current_user), db: Session = Depends(get_db)): return db.query(AcademicYear).order_by(AcademicYear.year_name).all()
@router.get("/current", response_model=AcademicYearResponse)
def current(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(AcademicYear).filter_by(is_current=True).first()
    if not row: raise HTTPException(404, "No current academic year")
    return row
@router.put("/{year_id}", response_model=AcademicYearResponse)
def update(year_id: int, data: AcademicYearUpdate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    row = db.get(AcademicYear, year_id)
    if not row: raise HTTPException(404, "Academic year not found")
    if data.is_current: db.query(AcademicYear).update({AcademicYear.is_current: False})
    for key, value in data.model_dump(exclude_none=True).items(): setattr(row, key, value)
    db.commit(); db.refresh(row); return row
