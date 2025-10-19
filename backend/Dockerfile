# Dockerfile (Development)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies (optional, for psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Default command (can be overridden in Compose)
CMD ["gunicorn", "api_football.wsgi:application", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "2", \
    "--timeout", "120", \
    "--reload", \
    "--log-level", "debug"]