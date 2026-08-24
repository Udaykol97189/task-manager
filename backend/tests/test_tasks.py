from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API"}


def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Learn automated testing",
            "description": "Write API tests with pytest",
            "priority": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Learn automated testing"
    assert data["description"] == "Write API tests with pytest"
    assert data["priority"] == 2
    assert data["completed"] is False
def test_get_tasks(client):
    client.post(
        "/tasks/",
        json={
            "title": "Task A",
            "description": "First task",
            "priority": 1,
        },
    )

    client.post(
        "/tasks/",
        json={
            "title": "Task B",
            "description": "Second task",
            "priority": 2,
        },
    )

    response = client.get("/tasks/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 2


def test_update_task(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Original title",
            "description": "Original description",
            "priority": 1,
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "priority": 3,
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Updated title"
    assert data["priority"] == 3
    assert data["completed"] is True


def test_delete_task(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Task to delete",
            "description": "This task will be deleted",
            "priority": 1,
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/tasks/{task_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 404


def test_create_task_validation(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Invalid priority",
            "description": "Priority should fail",
            "priority": 5,
        },
    )

    assert response.status_code == 422


def test_update_task_validation(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Validation test",
            "priority": 1,
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "priority": 5,
        },
    )

    assert response.status_code == 422

def test_filter_tasks_by_completed(client):
    client.post(
        "/tasks/",
        json={"title": "Incomplete task", "priority": 1},
    )

    create_response = client.post(
        "/tasks/",
        json={"title": "Completed task", "priority": 2},
    )

    task_id = create_response.json()["id"]

    client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    response = client.get("/tasks/?completed=true")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["completed"] is True


def test_filter_tasks_by_priority(client):
    client.post(
        "/tasks/",
        json={"title": "Low priority", "priority": 1},
    )

    client.post(
        "/tasks/",
        json={"title": "High priority", "priority": 3},
    )

    response = client.get("/tasks/?priority=3")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["priority"] == 3


def test_task_pagination(client):
    for i in range(5):
        client.post(
            "/tasks/",
            json={
                "title": f"Task {i}",
                "priority": 1,
            },
        )

    response = client.get("/tasks/?skip=1&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


def test_task_sorting_ascending(client):
    client.post(
        "/tasks/",
        json={"title": "Priority 3", "priority": 3},
    )

    client.post(
        "/tasks/",
        json={"title": "Priority 1", "priority": 1},
    )

    client.post(
        "/tasks/",
        json={"title": "Priority 2", "priority": 2},
    )

    response = client.get(
        "/tasks/?sort_by=priority&sort_order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    priorities = [task["priority"] for task in data]

    assert priorities == [1, 2, 3]


def test_task_sorting_descending(client):
    client.post(
        "/tasks/",
        json={"title": "Priority 1", "priority": 1},
    )

    client.post(
        "/tasks/",
        json={"title": "Priority 3", "priority": 3},
    )

    client.post(
        "/tasks/",
        json={"title": "Priority 2", "priority": 2},
    )

    response = client.get(
        "/tasks/?sort_by=priority&sort_order=desc"
    )

    assert response.status_code == 200

    data = response.json()

    priorities = [task["priority"] for task in data]

    assert priorities == [3, 2, 1]

def test_invalid_sort_field(client):
    response = client.get(
        "/tasks/?sort_by=password"
    )

    assert response.status_code == 422


def test_invalid_sort_order(client):
    response = client.get(
        "/tasks/?sort_order=invalid"
    )

    assert response.status_code == 422


def test_invalid_limit(client):
    response = client.get(
        "/tasks/?limit=101"
    )

    assert response.status_code == 422


def test_invalid_skip(client):
    response = client.get(
        "/tasks/?skip=-1"
    )

    assert response.status_code == 422


def test_get_nonexistent_task(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task 999999 not found"
    }