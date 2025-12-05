from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    todos = relationship("TodoModel", back_populates="owner")

class TodoModel(Base):
    """SQLAlchemy model for Todo items"""
    __tablename__ = "todos"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(BigInteger, nullable=False)  # Timestamp in milliseconds
    due_date = Column(BigInteger, nullable=True)  # Timestamp in milliseconds
    priority = Column(String, nullable=True)  # "low", "medium", "high"
    category = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    owner = relationship("User", back_populates="todos")
