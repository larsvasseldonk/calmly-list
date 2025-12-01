from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TodoBase(BaseModel):
    text: str
    dueDate: Optional[int] = Field(None, description="Timestamp in milliseconds")
    priority: Optional[Priority] = None
    category: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None
    dueDate: Optional[int] = Field(None, description="Timestamp in milliseconds")
    priority: Optional[Priority] = None
    category: Optional[str] = None

class Todo(TodoBase):
    id: str
    completed: bool
    createdAt: int = Field(..., description="Timestamp in milliseconds")

    model_config = ConfigDict(from_attributes=True)
