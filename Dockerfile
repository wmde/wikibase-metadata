



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

# Create a directory for logs TODO: do not write to container file system
RUN mkdir /app/logs

# Security: run as non-root
RUN useradd -u 10001 -m appuser
RUN chown 10001 /app/logs
USER appuser

# Expose the backend port
EXPOSE 8080

# Run the backend, 4 cores * 2 + 1
CMD ["gunicorn","app:app","-k","uvicorn.workers.UvicornWorker","--workers","9","-b","0.0.0.0:8080"]
