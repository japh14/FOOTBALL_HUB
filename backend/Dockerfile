# Dockerfile (Development)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Run migrations and collect static files on startup
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn api_football.wsgi:application --bind 0.0.0.0:8000 --workers 2 --reload --timeout 120 --log-level debug