from fastapi import FastAPI
from app.api.tasks import router as task_router
app = FastAPI()

# We add task route 
app.include_router(task_router)

@app.get("/")
def read_root():
    return {"message": "Task Manager API"}