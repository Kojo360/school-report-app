"""PostgreSQL database configuration and SQLAlchemy session utilities."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/ges_assessment",
)


class Base(DeclarativeBase):
    """Base class shared by every database model."""


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """Yield a database session and close it once the request is complete."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
