"""Idempotent seed data for a new GES assessment database."""

from sqlalchemy import select

from app.models.academic_year import AcademicYear
from app.models.class_model import ClassModel
from app.models.role import Role
from app.models.subject import Subject
from app.models.term import Term
from app.models.user import User
from app.core.security import hash_password

ROLES = ["Administrator", "Headmaster", "Teacher"]
SUBJECTS = [("ENG", "English Language"), ("MAT", "Mathematics"), ("SCI", "Science"), ("ICT", "Information and Communication Technology"), ("RME", "Religious and Moral Education"), ("FRT", "French"), ("GH", "Ghanaian Language"), ("CRE", "Creative Arts"), ("PE", "Physical Education"), ("OWOP", "Our World Our People")]
CLASSES = [f"Basic {number}" for number in range(1, 7)] + [f"JHS {number}" for number in range(1, 4)]


def seed_database(session) -> None:
    """Create reference data and an administrator account without duplicates."""
    for name in ROLES:
        if session.scalar(select(Role).where(Role.name == name)) is None:
            session.add(Role(name=name))
    for code, name in SUBJECTS:
        if session.scalar(select(Subject).where(Subject.code == code)) is None:
            session.add(Subject(code=code, name=name))
    for name in CLASSES:
        if session.scalar(select(ClassModel).where(ClassModel.name == name)) is None:
            session.add(ClassModel(name=name))
    session.flush()

    year = session.scalar(select(AcademicYear).where(AcademicYear.year_name == "2026/2027"))
    if year is None:
        year = AcademicYear(year_name="2026/2027", is_current=True)
        session.add(year); session.flush()
    for number in (1, 2, 3):
        name = f"Term {number}"
        if session.scalar(select(Term).where(Term.academic_year_id == year.id, Term.name == name)) is None:
            session.add(Term(academic_year_id=year.id, name=name, is_open=(number == 3)))

    admin_role = session.scalar(select(Role).where(Role.name == "Administrator"))
    accounts = [("admin", "admin@ges.local", "Administrator"), ("headmaster", "headmaster@ges.local", "Headmaster"), ("teacher1", "teacher1@ges.local", "Teacher")]
    for username, email, role_name in accounts:
        if session.scalar(select(User).where(User.username == username)) is None:
            role = session.scalar(select(Role).where(Role.name == role_name))
            session.add(User(username=username, email=email, password_hash=hash_password("ChangeMeImmediately!"), role_id=role.id, is_active=True))
    session.commit()
