from datetime import UTC, datetime, timedelta
from enum import Enum

import jwt
from passlib.context import CryptContext

from app.core.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET_KEY

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRole(str, Enum):
    ADMINISTRATOR = "Administrator"
    HEADMASTER = "Headmaster"
    TEACHER = "Teacher"

def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)

def create_access_token(username: str, role: UserRole) -> str:
    return jwt.encode({"sub": username, "role": role.value, "exp": datetime.now(UTC) + timedelta(minutes=JWT_EXPIRE_MINUTES)}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
