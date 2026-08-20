from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.tasks import router as task_router
from app.exceptions.task_exceptions import TaskNotFoundError


app = FastAPI()


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


app.include_router(task_router)


@app.get("/")
def read_root():
    return {"message": "Task Manager API"}