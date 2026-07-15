from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_admin
from app.database import get_db
from app.models.subject import Subject
from app.models.user import User
from app.schemas.academic import SubjectCreate, SubjectResponse
router=APIRouter(prefix="/subjects",tags=["Subjects"])
@router.post("",response_model=SubjectResponse)
def create(data:SubjectCreate,_:User=Depends(require_admin),db:Session=Depends(get_db)):
    if db.query(Subject).filter((Subject.code==data.code)|(Subject.name==data.name)).first(): raise HTTPException(409,"Subject already exists")
    row=Subject(**data.model_dump());db.add(row);db.commit();db.refresh(row);return row
@router.get("",response_model=list[SubjectResponse])
def list_all(_:User=Depends(get_current_user),db:Session=Depends(get_db)): return db.query(Subject).order_by(Subject.code).all()
@router.put("/{subject_id}",response_model=SubjectResponse)
def update(subject_id:int,data:SubjectCreate,_:User=Depends(require_admin),db:Session=Depends(get_db)):
    row=db.get(Subject,subject_id)
    if not row: raise HTTPException(404,"Subject not found")
    row.code=data.code;row.name=data.name;db.commit();db.refresh(row);return row
@router.delete("/{subject_id}",status_code=204)
def delete(subject_id:int,_:User=Depends(require_admin),db:Session=Depends(get_db)):
    row=db.get(Subject,subject_id)
    if not row: raise HTTPException(404,"Subject not found")
    db.delete(row);db.commit()
