# Calmly List

A modern, full-stack Todo application built with React, FastAPI, and SQLite.

## Features

- **User Authentication**: Secure registration and login using JWT.
- **Task Management**: Create, read, update, and delete tasks.
- **Categorization**: Organize tasks by category.
- **Prioritization**: Set priority levels (Low, Medium, High).
- **Due Dates**: Set and track due dates for tasks.
- **Filtering**: Filter tasks by status (All, Active, Completed).
- **Search**: Real-time search functionality.
- **Responsive Design**: Beautiful UI built with Tailwind CSS and Shadcn UI.

## Tech Stack

### Frontend
- **React**: UI library
- **TypeScript**: Static typing
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Shadcn UI**: Component library
- **React Query**: Data fetching
- **React Router**: Navigation

### Backend
- **FastAPI**: Web framework
- **Python**: Programming language
- **SQLAlchemy**: ORM
- **SQLite**: Database
- **PyJWT**: JWT authentication
- **Argon2**: Password hashing

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.12+)
- `uv` (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd calmly-list
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   uv sync
   cd ..
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

You can run both the frontend and backend concurrently from the root directory:

```bash
npm run dev
```

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Running Individually

**Backend:**
```bash
cd backend
uv run uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## Project Structure

- `backend/`: FastAPI application code
  - `app/`: Main application logic (API, models, schemas, auth)
  - `tests/`: Unit tests
  - `tests_integration/`: Integration tests
- `frontend/`: React application code
  - `src/`: Source code (components, pages, context, api)
- `openapi.yaml`: OpenAPI specification

## License

MIT
