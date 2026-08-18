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


def get_all(db: Session) -> list[Task]:
    return db.query(Task).all()


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