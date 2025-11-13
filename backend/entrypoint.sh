#! /usr/bin/bash

alembic upgrade head && \
pytest -m data && \
gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 9 -b 0.0.0.0:8000 --preload
