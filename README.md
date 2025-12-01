# Calmly List

A simple, elegant Todo application built with Django and React.

## Features
- **Create, Read, Update, Delete** todos.
- **Filter** by active/completed status.
- **Search** functionality.
- **Priorities** and **Categories**.
- **Due Dates**.
- **Persistent Storage** using SQLite.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Frontend**: React, TypeScript, Tailwind CSS, Shadcn UI
- **Database**: SQLite

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- `uv` (Python package manager)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/larsvasseldonk/calmly-list.git
    cd calmly-list
    ```

2.  Install dependencies:
    ```bash
    make install
    ```

### Running the App

Run both backend and frontend concurrently:
```bash
make dev
```

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### Testing

Run backend tests:
```bash
make test
```
