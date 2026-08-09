# Project Requirements

## 1. Project Overview

Docker Task Manager is a web-based task management application.

The application allows users to create, view, update, complete,
and delete tasks.

## 2. Functional Requirements

### FR-01: Create Task

The system must allow a user to create a task.

A task must contain:

- title
- description
- priority

The system will automatically generate:

- id
- status
- created_at
- updated_at

### FR-02: List Tasks

The system must allow users to retrieve all tasks.

### FR-03: Get Task

The system must allow users to retrieve a single task by ID.

### FR-04: Update Task

The system must allow users to update an existing task.

### FR-05: Delete Task

The system must allow users to delete an existing task.

### FR-06: Complete Task

The system must allow users to mark a task as completed.

### FR-07: Filter Tasks

The system should allow users to filter tasks by:

- status
- priority

## 3. Task Status

A task can have the following statuses:

- pending
- completed

## 4. Task Priority

A task can have the following priorities:

- low
- medium
- high

## 5. Non-Functional Requirements

### Maintainability

The backend should use clear separation between:

- API layer
- service layer
- database layer

### Validation

Invalid input must be rejected by the backend.

### Error Handling

The API must return appropriate HTTP status codes
and meaningful error responses.

### Testing

Backend functionality must have automated tests.

### Containerization

The complete application must be runnable using Docker Compose.

### Configuration

Environment-specific configuration must not be hardcoded
inside the application.

### Security

The application should follow basic production security
practices.

## 6. Initial API

POST   /api/v1/tasks
GET    /api/v1/tasks
GET    /api/v1/tasks/{id}
PUT    /api/v1/tasks/{id}
DELETE /api/v1/tasks/{id}
PATCH  /api/v1/tasks/{id}/complete

## 7. Future Scope

The initial version does not include authentication.

Future versions may include:

- user authentication
- authorization
- pagination
- search
- task ownership
- logging
- monitoring
- CI/CD
- production deployment