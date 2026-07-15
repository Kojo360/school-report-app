from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.core.security import UserRole, create_access_token, verify_password
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if user is None or not user.is_active or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    role = UserRole(user.role.name)
    return {"access_token": create_access_token(user.username, role), "token_type": "bearer", "user": {"id": user.id, "username": user.username, "role": role.value}}

@router.get("/me")
def current_user(user: User = Depends(get_current_user)):
    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role.name, "is_active": user.is_active}

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(_: User = Depends(get_current_user)):
    """Stateless logout: the client discards its JWT; token expiry limits reuse."""
