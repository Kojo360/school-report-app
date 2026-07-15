from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_admin
from app.database import get_db
from app.models.class_model import ClassModel
from app.models.teacher import Teacher
from app.models.user import User
from app.schemas.academic import ClassCreate, ClassResponse
router=APIRouter(prefix="/classes",tags=["Classes"])
@router.post("",response_model=ClassResponse)
def create(data:ClassCreate,_:User=Depends(require_admin),db:Session=Depends(get_db)):
    if db.query(ClassModel).filter_by(name=data.name).first(): raise HTTPException(409,"Class already exists")
    row=ClassModel(**data.model_dump());db.add(row);db.commit();db.refresh(row);return row
@router.get("",response_model=list[ClassResponse])
def list_all(_:User=Depends(get_current_user),db:Session=Depends(get_db)): return db.query(ClassModel).order_by(ClassModel.name).all()
@router.put("/{class_id}/teacher",response_model=ClassResponse)
def assign_teacher(class_id:int,teacher_id:int,_:User=Depends(require_admin),db:Session=Depends(get_db)):
    row=db.get(ClassModel,class_id)
    if not row: raise HTTPException(404,"Class not found")
    if not db.get(Teacher,teacher_id): raise HTTPException(404,"Teacher not found")
    row.teacher_id=teacher_id;db.commit();db.refresh(row);return row
