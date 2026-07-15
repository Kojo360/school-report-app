from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.teacher import router as teacher_router
from app.routes.sync import router as sync_router
from app.routes.reports import router as reports_router

app = FastAPI(
    title="GES Assessment API"
)
app.include_router(auth_router)
app.include_router(teacher_router)
app.include_router(sync_router)
app.include_router(reports_router)


@app.get("/")
def home():

    return {
        "message":"GES API Running"
    }
