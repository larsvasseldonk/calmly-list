from typing import List, Optional
from app.models import Todo, TodoCreate, TodoUpdate
import time
import uuid

# Mock database
db: List[Todo] = []

def get_todos() -> List[Todo]:
    return db

def get_todo(todo_id: str) -> Optional[Todo]:
    for todo in db:
        if todo.id == todo_id:
            return todo
    return None

def create_todo(todo_create: TodoCreate) -> Todo:
    new_todo = Todo(
        id=str(uuid.uuid4()),
        text=todo_create.text,
        completed=False,
        createdAt=int(time.time() * 1000),
        dueDate=todo_create.dueDate,
        priority=todo_create.priority,
        category=todo_create.category
    )
    db.append(new_todo)
    return new_todo

def update_todo(todo_id: str, todo_update: TodoUpdate) -> Optional[Todo]:
    todo = get_todo(todo_id)
    if not todo:
        return None
    
    update_data = todo_update.model_dump(exclude_unset=True)
    updated_todo = todo.model_copy(update=update_data)
    
    # Replace in db
    for i, t in enumerate(db):
        if t.id == todo_id:
            db[i] = updated_todo
            break
            
    return updated_todo

def delete_todo(todo_id: str) -> bool:
    for i, todo in enumerate(db):
        if todo.id == todo_id:
            db.pop(i)
            return True
    return False

def delete_completed_todos() -> int:
    global db
    initial_count = len(db)
    db = [todo for todo in db if not todo.completed]
    return initial_count - len(db)
