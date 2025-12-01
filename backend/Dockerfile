FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps as root for proper site-packages install
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt

# Copy backend + app code (use .dockerignore to keep this lean)
COPY . .

# Create non-root user and give it ownership of the app dir + data
RUN useradd -u 10001 -m appuser \
    && mkdir -p ./data/gx/plugins \
    && mkdir -p ./data/gx/uncommitted \
    && chown -R appuser:appuser /app

USER appuser

# Expose the backend port
EXPOSE 8000

CMD ["./start.sh"]
