from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Todo, TodoCreate, TodoUpdate, UserCreate
from app.schema import TodoModel, User
from app.auth import get_password_hash
import time
import uuid


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, user_id: str) -> List[Todo]:
    """Get all todos for a specific user"""
    db_todos = db.query(TodoModel).filter(TodoModel.user_id == user_id).all()
    return [
        Todo(
            id=todo.id,
            text=todo.text,
            completed=todo.completed,
            createdAt=todo.created_at,
            dueDate=todo.due_date,
            priority=todo.priority,
            category=todo.category,
            user_id=todo.user_id
        )
        for todo in db_todos
    ]


def get_todo(db: Session, todo_id: str, user_id: str) -> Optional[Todo]:
    """Get a single todo by ID and user"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id, TodoModel.user_id == user_id).first()
    if not db_todo:
        return None
    
    return Todo(
        id=db_todo.id,
        text=db_todo.text,
        completed=db_todo.completed,
        createdAt=db_todo.created_at,
        dueDate=db_todo.due_date,
        priority=db_todo.priority,
        category=db_todo.category,
        user_id=db_todo.user_id
    )


def create_todo(db: Session, todo_create: TodoCreate, user_id: str) -> Todo:
    """Create a new todo for a user"""
    db_todo = TodoModel(
        id=str(uuid.uuid4()),
        text=todo_create.text,
        completed=False,
        created_at=int(time.time() * 1000),
        due_date=todo_create.dueDate,
        priority=todo_create.priority.value if todo_create.priority else None,
        category=todo_create.category,
        user_id=user_id
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
        category=db_todo.category,
        user_id=db_todo.user_id
    )


def update_todo(db: Session, todo_id: str, todo_update: TodoUpdate, user_id: str) -> Optional[Todo]:
    """Update an existing todo for a user"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id, TodoModel.user_id == user_id).first()
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
        category=db_todo.category,
        user_id=db_todo.user_id
    )


def delete_todo(db: Session, todo_id: str, user_id: str) -> bool:
    """Delete a todo by ID and user"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id, TodoModel.user_id == user_id).first()
    if not db_todo:
        return False
    
    db.delete(db_todo)
    db.commit()
    return True


def delete_completed_todos(db: Session, user_id: str) -> int:
    """Delete all completed todos for a user"""
    result = db.query(TodoModel).filter(TodoModel.completed == True, TodoModel.user_id == user_id).delete()
    db.commit()
    return result
