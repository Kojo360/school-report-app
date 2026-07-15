from collections.abc import Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import UserRole, decode_access_token
from app.database import get_db
from app.models.user import User

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token") from error
    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unavailable")
    return user

def require_roles(*roles: UserRole) -> Callable:
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.name not in {role.value for role in roles}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return checker

require_admin = require_roles(UserRole.ADMINISTRATOR)
require_headmaster = require_roles(UserRole.HEADMASTER, UserRole.ADMINISTRATOR)
require_teacher = require_roles(UserRole.TEACHER, UserRole.ADMINISTRATOR)
