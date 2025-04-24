from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..services.task_service import TaskService
from ..schemas.schemas import TaskCreate, TaskUpdate, Task
from ..repository.db import get_db

router = APIRouter(prefix="/tasks", tags=["Задачи"])

def get_task_service(db: Session = Depends(get_db)):
    return TaskService(db)

@router.post("/", response_model=Task, summary="Создать новую задачу")
def create_task(task_in: TaskCreate, service: TaskService = Depends(get_task_service)):
    """
    Создаёт новую задачу со всеми необходимыми параметрами.
    """
    return service.create_task(task_in)

@router.get("/{task_id}", response_model=Task, summary="Получить задачу по ID")
def read_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """
    Возвращает задачу с указанным ID.
    """
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=List[Task], summary="Получить список задач с фильтрами")
def read_tasks(
    due_date: Optional[datetime] = Query(None, description="Фильтр по сроку выполнения (до этой даты)"),
    status: Optional[bool] = Query(None, description="Фильтр по статусу выполнения"),
    service: TaskService = Depends(get_task_service)
):
    """
    Возвращает список задач, отфильтрованных по дате и/или статусу.
    Если фильтры не заданы, возвращаются все задачи.
    """
    return service.get_tasks(due_date, status)

@router.put("/{task_id}", response_model=Task, summary="Обновить задачу по ID")
def update_task(task_id: int, task_in: TaskUpdate, service: TaskService = Depends(get_task_service)):
    """
    Обновляет данные задачи с указанным ID.
    """
    task = service.update_task(task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", response_model=dict, summary="Удалить задачу по ID")
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """
    Удаляет задачу с указанным ID.
    """
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}