# Development container for local development of the app.
# Accompanied by a docker compose file for conveniently mounting 
# the project directory into the container and opening ports.

FROM python:3.10.12-slim

RUN mkdir /workspace
WORKDIR /workspace

COPY ./requirements*.txt /workspace

RUN pip install -r requirements.txt -r requirements-dev.txt

ENV PYTHONPATH="/workspace"

ENTRYPOINT ["fastapi"]
CMD ["dev", "app.py", "--host", "0.0.0.0"]
