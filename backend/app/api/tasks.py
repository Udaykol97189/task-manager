from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("/")
def get_tasks():
    return {"message": "Task endpoint is working"}