from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
    status: Optional[bool]

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    status: bool