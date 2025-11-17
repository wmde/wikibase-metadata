#! /usr/bin/bash

alembic upgrade head && \
PYTHONPATH=. pytest -m data -p no:cacheprovider && \
gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 9 -b 0.0.0.0:8000 --preload
