FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps first for caching
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend + app code (use .dockerignore to keep this lean)
COPY . .

# Security: run as non-root
RUN useradd -u 10001 -m appuser
USER appuser

# Expose the backend port
EXPOSE 8000

CMD ["./start.sh"]
