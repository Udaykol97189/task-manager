import pytest
from app.models.task import Task
from app.repositories.task_repository import (
    create,
    delete,
    get_all,
    get_by_id,
    update,
)


def test_create_repository(db_session):
    task = Task(
        title="Repository create test",
        description="Testing repository create",
        priority=2,
    )

    result = create(db_session, task)

    assert result.id is not None
    assert result.title == "Repository create test"
    assert result.priority == 2


def test_get_by_id_repository(db_session):
    task = Task(
        title="Repository get test",
        description="Testing get by id",
        priority=1,
    )

    created_task = create(db_session, task)

    result = get_by_id(db_session, created_task.id)

    assert result is not None
    assert result.id == created_task.id
    assert result.title == "Repository get test"


def test_get_by_id_repository_not_found(db_session):
    result = get_by_id(db_session, 999999)

    assert result is None


def test_update_repository(db_session):
    task = Task(
        title="Original repository task",
        description="Original description",
        priority=1,
    )

    created_task = create(db_session, task)

    created_task.title = "Updated repository task"
    created_task.priority = 3

    result = update(db_session, created_task)

    assert result.title == "Updated repository task"
    assert result.priority == 3


def test_delete_repository(db_session):
    task = Task(
        title="Repository delete test",
        description="Testing delete",
        priority=1,
    )

    created_task = create(db_session, task)
    task_id = created_task.id

    delete(db_session, created_task)

    result = get_by_id(db_session, task_id)

    assert result is None


def test_get_all_filter_by_priority(db_session):
    create(
        db_session,
        Task(title="Low priority", priority=1),
    )
    create(
        db_session,
        Task(title="High priority", priority=3),
    )

    result = get_all(
        db_session,
        priority=3,
    )

    assert len(result) == 1
    assert result[0].title == "High priority"


def test_get_all_filter_by_completed(db_session):
    incomplete_task = Task(
        title="Incomplete",
        priority=1,
        completed=False,
    )

    completed_task = Task(
        title="Completed",
        priority=1,
        completed=True,
    )

    create(db_session, incomplete_task)
    create(db_session, completed_task)

    result = get_all(
        db_session,
        completed=True,
    )

    assert len(result) == 1
    assert result[0].title == "Completed"


def test_get_all_pagination(db_session):
    for i in range(5):
        create(
            db_session,
            Task(
                title=f"Task {i}",
                priority=1,
            ),
        )

    result = get_all(
        db_session,
        skip=1,
        limit=2,
    )

    assert len(result) == 2


def test_get_all_sorting_ascending(db_session):
    create(db_session, Task(title="Priority 3", priority=3))
    create(db_session, Task(title="Priority 1", priority=1))
    create(db_session, Task(title="Priority 2", priority=2))

    result = get_all(
        db_session,
        sort_by="priority",
        sort_order="asc",
    )

    priorities = [task.priority for task in result]

    assert priorities == [1, 2, 3]


def test_get_all_sorting_descending(db_session):
    create(db_session, Task(title="Priority 1", priority=1))
    create(db_session, Task(title="Priority 3", priority=3))
    create(db_session, Task(title="Priority 2", priority=2))

    result = get_all(
        db_session,
        sort_by="priority",
        sort_order="desc",
    )

    priorities = [task.priority for task in result]

    assert priorities == [3, 2, 1]

def test_get_all_invalid_sort_field(db_session):
    try:
        get_all(
            db_session,
            sort_by="password",
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Invalid sort field: password"

def test_get_all_invalid_sort_field(db_session):
    with pytest.raises(
        ValueError,
        match="Invalid sort field: password",
    ):
        get_all(
            db_session,
            sort_by="password",
        )