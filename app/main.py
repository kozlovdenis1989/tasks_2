from fastapi import FastAPI
from .routers import task_router
from .repository import db

app = FastAPI(title="Список задач")

app.include_router(task_router.router)

@app.on_event("startup")
def startup():
    db.create_tables()

