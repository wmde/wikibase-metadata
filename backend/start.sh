#!/usr/bin/env bash

# Migrate and check data integrity
alembic upgrade head && pytest -m data

# Run the backend, 4 cores * 2 + 1
gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 9 -b 0.0.0.0:8000 --preload
