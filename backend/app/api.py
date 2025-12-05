from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from app.models import Todo, TodoCreate, TodoUpdate, UserCreate, UserResponse, Token
from app import db, auth
from app.database import get_db
from app.schema import User
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db_session: Session = Depends(get_db)):
    db_user = db.get_user_by_email(db_session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db.create_user(db_session, user=user)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
    user = db.get_user_by_email(db_session, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/todos", response_model=List[Todo])
def get_todos(
    db_session: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    return db.get_todos(db_session, user_id=current_user.id)

@router.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate, 
    db_session: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    return db.create_todo(db_session, todo, user_id=current_user.id)

@router.patch("/todos/{id}", response_model=Todo)
def update_todo(
    id: str, 
    todo_update: TodoUpdate, 
    db_session: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    updated_todo = db.update_todo(db_session, id, todo_update, user_id=current_user.id)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/todos/completed", status_code=status.HTTP_204_NO_CONTENT)
def delete_completed_todos(
    db_session: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    db.delete_completed_todos(db_session, user_id=current_user.id)
    return

@router.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    id: str, 
    db_session: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    if not db.delete_todo(db_session, id, user_id=current_user.id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return
