# Universal entry point for the fastapi_react_tutorial monorepo (backend + frontend).
# Run `make` (or `make help`) to see the targets.
SHELL := /bin/bash

.PHONY: help install dev backend frontend build start host test clean

help:
	@echo "make install   install backend (uv) + frontend (npm) dependencies"
	@echo "make dev       run backend (:8000) + frontend (:5173) together, hot-reload"
	@echo "make start     build the frontend, then serve API + UI from ONE server (:8000)"
	@echo "make host      like start, but bound to the LAN → http://<this-machine>.local:<port>"
	@echo "make build     build the frontend for production (frontend/dist)"
	@echo "make test      backend tests + ruff + a frontend build check"
	@echo "make clean     remove build artifacts and caches"

install:
	cd backend && uv sync
	cd frontend && npm install

# Development: both servers, one command, one Ctrl-C. The browser loads the app from
# Vite (:5173) and the app calls the API at :8000/api cross-origin (handled by CORS).
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

# LAN host: like `start`, but the launcher binds 0.0.0.0 (all interfaces) so other
# devices on the same Wi-Fi can reach it, auto-picks a free port, and prints the
# machine's real <name>.local URL. Override HOST=127.0.0.1 (local only) or PORT=8080.
# `--no-sync` so just running the host never rewrites uv.lock.
host: build
	cd backend && uv run --no-sync python host.py

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
