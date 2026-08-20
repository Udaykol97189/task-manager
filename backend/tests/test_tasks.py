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

    assert response.status_code == 200

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

    assert create_response.status_code == 200

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

    assert create_response.status_code == 200

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

    assert create_response.status_code == 200

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "priority": 5,
        },
    )

    assert response.status_code == 422