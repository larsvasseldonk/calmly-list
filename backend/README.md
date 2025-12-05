# Calmly List Backend

This is the FastAPI backend for the Calmly List application.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management

## Installation

Install dependencies:

```bash
uv sync
```

## Running the Application

You can run both the frontend and backend concurrently from the root directory:

```bash
npm run dev
```

- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Running Individually

To run just the backend:
```bash
cd backend
uv run uvicorn app.main:app --reload
```

To run just the frontend:
```bash
cd frontend
npm run dev
```

## Database

The application uses SQLite for persistent storage. The database file `todos.db` is automatically created in the backend directory when the server starts. Todo items are persisted across server restarts.

## Running Tests

> **Note**: There is currently a known issue with the test suite where the test database engine  configuration is not properly overriding the production engine due to module-level initialization timing. The production code works correctly with SQLite. This will be addressed in a future update.

Run the test suite:

```bash
uv run pytest
```

## Project Structure

- `app/`: Application source code
    - `main.py`: Application entry point and FastAPI app configuration
    - `api.py`: API endpoints
    - `models.py`: Pydantic models for request/response validation
    - `database.py`: SQLAlchemy database configuration
    - `schema.py`: SQLAlchemy ORM models  
    - `db.py`: Database operations (CRUD)
- `tests/`: Test suite
