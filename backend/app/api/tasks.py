from app.models.task import Task
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
    create_task,
    get_task,
    get_tasks,
    update_task,
    delete_task
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

def apply_task_updates(task: Task, task_data: TaskUpdate) -> Task:
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    return task

@router.post("/", response_model=TaskResponse)
def create_task_endpoint(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db, task_data)


@router.get("/", response_model=list[TaskResponse])
def get_tasks_endpoint(
    db: Session = Depends(get_db),
):
    return get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
):
    return get_task(db, task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)

    return update_task(db, task, task_data)

@router.delete("/{task_id}", status_code=204)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)

    delete_task(db, task)