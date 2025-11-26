FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps first for caching
COPY requirements.txt ./requirements.txt
COPY requirements-dev.txt ./requirements-dev.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy backend + app code (use .dockerignore to keep this lean)
COPY . .

# Need to be writable during database checks
RUN chown 10001 -R ./data/gx/plugins
RUN mkdir ./data/gx/uncommitted
RUN chown 10001 -R ./data/gx/uncommitted

# Security: run as non-root
RUN useradd -u 10001 -m appuser
USER appuser

# Expose the backend port
EXPOSE 8000
