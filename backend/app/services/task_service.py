from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.exceptions.task_exceptions import TaskNotFoundError
from app.repositories.task_repository import (
    create,
    delete,
    get_all,
    get_by_id,
    update,
)


def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
    )

    return create(db, task)


def get_tasks(db: Session) -> list[Task]:
    return get_all(db)


def get_task(db: Session, task_id: int) -> Task:
    task = get_by_id(db, task_id)

    if task is None:
        raise TaskNotFoundError(f"Task {task_id} not found")

    return task


def apply_task_updates(task: Task, task_data: TaskUpdate) -> Task:
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    return task


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate,
) -> Task:
    task = apply_task_updates(task, task_data)

    return update(db, task)


def delete_task(db: Session, task: Task) -> None:
    delete(db, task)