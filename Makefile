# Universal entry point for the rag_system monorepo (backend + frontend).
# Run `make` (or `make help`) to see the targets.
SHELL := /bin/bash

.PHONY: help install dev backend frontend build start test clean

help:
	@echo "make install   install backend (uv) + frontend (npm) dependencies"
	@echo "make dev       run backend (:8000) + frontend (:5173) together, hot-reload"
	@echo "make start     build the frontend, then serve API + UI from ONE server (:8000)"
	@echo "make build     build the frontend for production (frontend/dist)"
	@echo "make test      backend tests + ruff + a frontend build check"
	@echo "make clean     remove build artifacts and caches"

install:
	cd backend && uv sync
	cd frontend && npm install

# Development: both servers, one command, one Ctrl-C. Vite proxies /api → :8000.
dev:
	@echo "backend  → http://127.0.0.1:8000"
	@echo "frontend → http://localhost:5173"
	@trap 'kill 0' EXIT INT TERM; \
	( cd backend && uv run uvicorn app.main:app --reload --port 8000 ) & \
	( cd frontend && npm run dev ) & \
	wait

# Production-style: one process serves the built UI and the API on :8000.
start: build
	@echo "serving API + UI → http://127.0.0.1:8000"
	cd backend && uv run uvicorn app.main:app

build:
	cd frontend && npm run build

backend:
	cd backend && uv run uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev

test:
	cd backend && uv run pytest && uv run ruff check
	cd frontend && npm run build

clean:
	rm -rf frontend/dist
	find backend -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
