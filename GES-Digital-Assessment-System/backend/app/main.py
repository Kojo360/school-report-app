from fastapi import APIRouter, FastAPI

from app.routes.auth import router as auth_router
from app.routes.teacher import router as teacher_router
from app.routes.sync import router as sync_router
from app.routes.reports import router as reports_router
from app.api.auth import router as modern_auth_router
from app.api.users import router as users_router
from app.api.students import router as students_router
from app.api.academic_years import router as academic_years_router
from app.api.terms import router as terms_router
from app.api.subjects import router as subjects_router
from app.api.classes import router as classes_router
from app.api.grades import router as grades_router

app = FastAPI(
    title="GES Assessment API"
)
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(modern_auth_router)
v1_router.include_router(teacher_router)
v1_router.include_router(sync_router)
v1_router.include_router(reports_router)
v1_router.include_router(users_router)
v1_router.include_router(students_router)
v1_router.include_router(academic_years_router)
v1_router.include_router(terms_router)
v1_router.include_router(subjects_router)
v1_router.include_router(classes_router)
v1_router.include_router(grades_router)

app.include_router(auth_router)
app.include_router(teacher_router)
app.include_router(sync_router)
app.include_router(reports_router)
app.include_router(modern_auth_router)
app.include_router(users_router)
app.include_router(students_router)
app.include_router(academic_years_router)
app.include_router(terms_router)
app.include_router(subjects_router)
app.include_router(classes_router)
app.include_router(grades_router)
app.include_router(v1_router)


@app.get("/")
def home():

    return {
        "message":"GES API Running"
    }
