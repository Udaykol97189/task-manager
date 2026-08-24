from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal

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


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task_endpoint(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db, task_data)


@router.get("/", response_model=list[TaskResponse])
def get_tasks_endpoint(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    completed: bool | None = None,
    priority: int | None = None,
    search: str | None = Query(default=None, min_length=1),
    sort_by: Literal[
        "created_at",
        "updated_at",
        "priority",
        "title",
        "completed",
    ] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
):
    return get_tasks(
        db,
        skip=skip,
        limit=limit,
        completed=completed,
        priority=priority,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )    


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