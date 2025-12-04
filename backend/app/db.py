from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Todo, TodoCreate, TodoUpdate
from app.schema import TodoModel
import time
import uuid


def get_todos(db: Session) -> List[Todo]:
    """Get all todos from the database"""
    db_todos = db.query(TodoModel).all()
    return [
        Todo(
            id=todo.id,
            text=todo.text,
            completed=todo.completed,
            createdAt=todo.created_at,
            dueDate=todo.due_date,
            priority=todo.priority,
            category=todo.category
        )
        for todo in db_todos
    ]


def get_todo(db: Session, todo_id: str) -> Optional[Todo]:
    """Get a single todo by ID"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        return None
    
    return Todo(
        id=db_todo.id,
        text=db_todo.text,
        completed=db_todo.completed,
        createdAt=db_todo.created_at,
        dueDate=db_todo.due_date,
        priority=db_todo.priority,
        category=db_todo.category
    )


def create_todo(db: Session, todo_create: TodoCreate) -> Todo:
    """Create a new todo in the database"""
    db_todo = TodoModel(
        id=str(uuid.uuid4()),
        text=todo_create.text,
        completed=False,
        created_at=int(time.time() * 1000),
        due_date=todo_create.dueDate,
        priority=todo_create.priority.value if todo_create.priority else None,
        category=todo_create.category
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    return Todo(
        id=db_todo.id,
        text=db_todo.text,
        completed=db_todo.completed,
        createdAt=db_todo.created_at,
        dueDate=db_todo.due_date,
        priority=db_todo.priority,
        category=db_todo.category
    )


def update_todo(db: Session, todo_id: str, todo_update: TodoUpdate) -> Optional[Todo]:
    """Update an existing todo"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        return None
    
    update_data = todo_update.model_dump(exclude_unset=True)
    
    # Map Pydantic field names to database column names
    if 'dueDate' in update_data:
        update_data['due_date'] = update_data.pop('dueDate')
    if 'priority' in update_data and update_data['priority'] is not None:
        update_data['priority'] = update_data['priority'].value
    
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    
    return Todo(
        id=db_todo.id,
        text=db_todo.text,
        completed=db_todo.completed,
        createdAt=db_todo.created_at,
        dueDate=db_todo.due_date,
        priority=db_todo.priority,
        category=db_todo.category
    )


def delete_todo(db: Session, todo_id: str) -> bool:
    """Delete a todo by ID"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        return False
    
    db.delete(db_todo)
    db.commit()
    return True


def delete_completed_todos(db: Session) -> int:
    """Delete all completed todos and return count deleted"""
    result = db.query(TodoModel).filter(TodoModel.completed == True).delete()
    db.commit()
    return result
