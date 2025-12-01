from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Todo, TodoCreate, TodoUpdate
from app import db

router = APIRouter()

@router.get("/todos", response_model=List[Todo])
def get_todos():
    return db.get_todos()

@router.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    return db.create_todo(todo)

@router.patch("/todos/{id}", response_model=Todo)
def update_todo(id: str, todo_update: TodoUpdate):
    updated_todo = db.update_todo(id, todo_update)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/todos/completed", status_code=status.HTTP_204_NO_CONTENT)
def delete_completed_todos():
    db.delete_completed_todos()
    return

@router.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: str):
    if not db.delete_todo(id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return
