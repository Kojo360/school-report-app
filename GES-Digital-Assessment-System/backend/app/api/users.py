from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import require_admin
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["users"])

def serialize(user: User) -> dict:
    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role.name, "is_active": user.is_active, "created_at": user.created_at}

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(payload: UserCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    try: return serialize(create_user(db, payload.username, payload.email, payload.password, payload.role))
    except ValueError as error: raise HTTPException(status_code=400, detail=str(error)) from error

@router.get("", response_model=list[UserResponse])
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return [serialize(user) for user in db.query(User).order_by(User.username).all()]

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None: raise HTTPException(status_code=404, detail="User not found")
    return serialize(user)

@router.patch("/{user_id}/disable", response_model=UserResponse)
def disable(user_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None: raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False; db.commit(); db.refresh(user)
    return serialize(user)
