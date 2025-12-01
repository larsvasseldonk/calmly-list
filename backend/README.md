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

## Running the Server

Start the development server:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive API documentation is available at `http://localhost:8000/docs`.

## Running Tests

Run the test suite:

```bash
uv run pytest
```

## Project Structure

- `app/`: Application source code
    - `main.py`: Application entry point
    - `api.py`: API endpoints
    - `models.py`: Pydantic models
    - `db.py`: Mock database implementation
- `tests/`: Test suite
