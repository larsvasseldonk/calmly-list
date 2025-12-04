import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import configure_test_db, SessionLocal, Base
from app.schema import TodoModel

# Use a file-based SQLite database for integration tests to ensure persistence behavior matches production
# and to avoid some in-memory specific issues.
TEST_DB_FILE = "./test_integration.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Configure test database once for all tests"""
    # Remove existing test db if it exists
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
        
    test_engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    # Configure the app to use this test engine
    configure_test_db(test_engine)
    
    yield
    
    # Cleanup after all tests
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

@pytest.fixture(scope="function", autouse=True)
def clear_db():
    """Clear database before each test"""
    db = SessionLocal()
    try:
        db.query(TodoModel).delete()
        db.commit()
    finally:
        db.close()
    yield

@pytest.fixture(scope="module")
def client():
    """Create test client"""
    with TestClient(app) as test_client:
        yield test_client
