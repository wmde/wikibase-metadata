web: alembic -x db_path=sqlite:///$TOOL_DATA_DIR/wikibase-data.db upgrade head && gunicorn app:app -k uvicorn.workers.UvicornWorker --workers=4 --timeout 60 --bind 0.0.0.0
