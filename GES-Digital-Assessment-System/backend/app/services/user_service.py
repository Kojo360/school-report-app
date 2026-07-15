from sqlalchemy.orm import Session
from app.core.security import UserRole, hash_password
from app.models.role import Role
from app.models.user import User

def create_user(db: Session, username: str, email: str, password: str, role_name: str) -> User:
    role = db.query(Role).filter(Role.name == role_name).first()
    if role is None or role_name not in {role.value for role in UserRole}:
        raise ValueError("Invalid role")
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise ValueError("Username or email already exists")
    user = User(username=username, email=email, password_hash=hash_password(password), role_id=role.id, is_active=True)
    db.add(user); db.commit(); db.refresh(user)
    return user
