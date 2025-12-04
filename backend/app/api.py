from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import Todo, TodoCreate, TodoUpdate
from app import db
from app.database import get_db

router = APIRouter()

@router.get("/todos", response_model=List[Todo])
def get_todos(db_session: Session = Depends(get_db)):
    return db.get_todos(db_session)

@router.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db_session: Session = Depends(get_db)):
    return db.create_todo(db_session, todo)

@router.patch("/todos/{id}", response_model=Todo)
def update_todo(id: str, todo_update: TodoUpdate, db_session: Session = Depends(get_db)):
    updated_todo = db.update_todo(db_session, id, todo_update)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/todos/completed", status_code=status.HTTP_204_NO_CONTENT)
def delete_completed_todos(db_session: Session = Depends(get_db)):
    db.delete_completed_todos(db_session)
    return

@router.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: str, db_session: Session = Depends(get_db)):
    if not db.delete_todo(db_session, id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return
