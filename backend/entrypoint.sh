#!/bin/bash
set e

alembic upgrade head && \
# PYTHONPATH=. python migrate.py && \
PYTHONPATH=. pytest -m data -p no:cacheprovider && \
exec gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 9 -b 0.0.0.0:8000
