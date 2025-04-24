from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.task import Task
from ..schemas.schemas import TaskCreate, TaskUpdate
from datetime import datetime

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_in: TaskCreate) -> Task:
        task = Task(**task_in.dict())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_tasks(self, due_date: Optional[datetime] = None, status: Optional[bool] = None) -> List[Task]:
        query = self.db.query(Task)
        if due_date:
            query = query.filter(Task.due_date <= due_date)
        if status is not None:
            query = query.filter(Task.status == status)
        return query.all()

    def update_task(self, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
        task = self.get_task(task_id)
        if not task:
            return None
        data = task_in.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True