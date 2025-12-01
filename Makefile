.PHONY: help install dev run-backend run-frontend test migrate migrations build clean

help:
	@echo "Available commands:"
	@echo "  make dev           - Run both backend and frontend concurrently"
	@echo "  make install       - Install backend and frontend dependencies"
	@echo "  make run-backend   - Run Django development server"
	@echo "  make run-frontend  - Run React development server"
	@echo "  make test          - Run backend tests"
	@echo "  make migrate       - Apply database migrations"
	@echo "  make migrations    - Create new database migrations"
	@echo "  make build         - Build frontend for production"
	@echo "  make clean         - Remove build artifacts and temporary files"

install:
	cd backend && uv sync
	cd frontend && npm install

dev:
	npm run dev

run-backend:
	cd backend && uv run python manage.py runserver

run-frontend:
	cd frontend && npm run dev

test:
	cd backend && uv run python manage.py test

migrate:
	cd backend && uv run python manage.py migrate

migrations:
	cd backend && uv run python manage.py makemigrations

build:
	cd frontend && npm run build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
