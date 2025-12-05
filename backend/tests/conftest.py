import pytest
from sqlalchemy import create_engine

from app.database import configure_test_db, SessionLocal, Base
from app.schema import TodoModel, User  # Import to register models
from fastapi.testclient import TestClient
from app.main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Configure test database once for all tests"""
    test_engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    print(f"DEBUG: setup_test_database calling configure_test_db. Tables: {Base.metadata.tables.keys()}")
    configure_test_db(test_engine)
    yield
    
@pytest.fixture(scope="function", autouse=True)
def clear_db():
    """Clear database before each test"""
    db = SessionLocal()
    try:
        db.query(TodoModel).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()
    yield

@pytest.fixture(scope="module")
def client():
    """Create test client"""
    with TestClient(app) as test_client:
        yield test_client
