from sqlalchemy import Column, String, Boolean, Integer
from app.database import Base
import uuid

class TodoModel(Base):
    """SQLAlchemy model for Todo items"""
    __tablename__ = "todos"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(Integer, nullable=False)  # Timestamp in milliseconds
    due_date = Column(Integer, nullable=True)  # Timestamp in milliseconds
    priority = Column(String, nullable=True)  # "low", "medium", "high"
    category = Column(String, nullable=True)
