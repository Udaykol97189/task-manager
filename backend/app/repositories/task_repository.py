from sqlalchemy.orm import Session

from app.models.task import Task


def create(db: Session, task: Task) -> Task:
    try:
        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    except Exception:
        db.rollback()
        raise


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    completed: bool | None = None,
    priority: int | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> list[Task]:
    query = db.query(Task)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    VALID_SORT_FIELDS = {
        "created_at",
        "updated_at",
        "priority",
        "title",
        "completed",
    }

    if sort_by not in VALID_SORT_FIELDS:
        raise ValueError(f"Invalid sort field: {sort_by}")

    sort_column = getattr(Task, sort_by)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def update(db: Session, task: Task) -> Task:
    try:
        db.commit()
        db.refresh(task)

        return task

    except Exception:
        db.rollback()
        raise


def delete(db: Session, task: Task) -> None:
    try:
        db.delete(task)
        db.commit()

    except Exception:
        db.rollback()
        raise