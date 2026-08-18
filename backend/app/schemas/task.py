from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=3)

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: int | None = Field(default=None, ge=1, le=3)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    priority: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)