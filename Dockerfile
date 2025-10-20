# -------------------- Stage 1: build frontend --------------------
FROM node:22-alpine AS frontend-builder
WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# -------------------- Stage 2: Python runtime --------------------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps first for caching
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend + app code (use .dockerignore to keep this lean)
COPY . .

# Bring in the built static assets to /app/dist
COPY --from=frontend-builder /app/dist ./dist

# Security: run as non-root
RUN useradd -u 10001 -m appuser
USER appuser

# Expose the backend port
EXPOSE 8000

# Run the backend, 4 cores * 2 + 1
CMD ["gunicorn","app:app","-k","uvicorn.workers.UvicornWorker","--workers","9","-b","0.0.0.0:8000","--preload"]
