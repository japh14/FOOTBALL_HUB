# Django REST Framework with Docker

A Django REST Framework API with JWT authentication, containerized with Docker.

---

## 🚀 Quick Start

### Prerequisites
- Docker installed on your machine
- Docker Compose installed

---

## 📦 Building and Running the Application

### Method 1: Verbose (Step-by-Step)

This method explicitly shows each step for better understanding:

```bash
# Step 1: Build the Docker images (specify the file explicitly)
docker compose -f docker-compose.yml build

# Step 2: Start the containers in detached mode
docker compose -f docker-compose.yml up -d
```

**What happens:**
- **Build step**: Docker reads your `Dockerfile` and `docker-compose.yml`, downloads base images, installs dependencies, and creates your custom images
- **Up step**: Docker creates containers from those images and starts them in the background (`-d` = detached mode)

---

### Method 2: Shortcut (Single Command)

For faster development, build and start in one command:

```bash
# Build and start in one command
docker compose up -d --build
```

**Note:** Use this after you've learned the steps above. This is the most common command during daily development.

---

## 🔧 Initial Setup

After starting the containers for the first time, run these commands:

```bash
# 1. Run database migrations
docker compose exec web python manage.py migrate

# 2. Create a superuser account
docker compose exec web python manage.py createsuperuser

# 3. (Optional) Collect static files for production
docker compose exec web python manage.py collectstatic --noinput
```

---

## 📋 Common Commands

### Container Management

```bash
# View running containers
docker compose ps

# View logs from all services
docker compose logs -f

# View logs from specific service (e.g., web)
docker compose logs -f web

# Stop containers (keeps them for restart)
docker compose stop

# Start existing containers (no rebuild)
docker compose start

# Stop and remove containers
docker compose down

# Stop, remove containers and volumes (fresh start)
docker compose down -v

# Restart a specific service
docker compose restart web
```

### Django Management Commands

```bash
# Run migrations
docker compose exec web python manage.py migrate

# Create migrations
docker compose exec web python manage.py makemigrations

# Create superuser
docker compose exec web python manage.py createsuperuser

# Access Django shell
docker compose exec web python manage.py shell

# Access container bash shell
docker compose exec web bash

# Run tests
docker compose exec web python manage.py test

# Check for issues
docker compose exec web python manage.py check
```

### Development Workflow

```bash
# After making code changes, rebuild and restart
docker compose up -d --build

# Or using verbose method:
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d

# View logs to debug
docker compose logs -f web

# Stop everything at end of day
docker compose down
```

---

## 🔐 API Authentication

This project uses JWT (JSON Web Token) authentication.

### Get Access Token (Login)

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use Access Token

```bash
curl http://localhost:8000/api/your-endpoint/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Refresh Token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## 📁 Project Structure

```
.
├── docker-compose.yml      # Docker services configuration
├── Dockerfile              # Docker image instructions
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
├── config/                # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/                   # Your API app
    ├── models.py
    ├── serializers.py
    ├── views.py
    └── urls.py
```

---

## 🐛 Troubleshooting

### Containers won't start
```bash
# Check container status
docker compose ps

# View error logs
docker compose logs

# Remove everything and start fresh
docker compose down -v
docker compose up -d --build
```

### Database connection issues
```bash
# Restart the database service
docker compose restart db

# Check database logs
docker compose logs db
```

### Port already in use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Need to reset database
```bash
# Stop and remove volumes
docker compose down -v

# Start fresh
docker compose up -d --build

# Run migrations again
docker compose exec web python manage.py migrate
```

---

## 🔄 Complete Rebuild (Fresh Start)

If you need to completely reset everything:

```bash
# Stop and remove all containers, networks, and volumes
docker compose down -v

# Remove all images (optional)
docker compose down --rmi all

# Rebuild from scratch
docker compose -f docker-compose.yml build --no-cache
docker compose -f docker-compose.yml up -d

# Run initial setup again
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

## 📚 Learning Resources

- **Django REST Framework**: https://www.django-rest-framework.org/
- **Docker Documentation**: https://docs.docker.com/
- **JWT Authentication**: https://django-rest-framework-simplejwt.readthedocs.io/

---

## 💡 Tips

1. **Always use `-d` flag** when running `docker compose up` to run containers in the background
2. **Check logs regularly** with `docker compose logs -f` to catch errors early
3. **Use `docker compose down -v`** when you need to reset the database
4. **Rebuild after dependency changes** (adding packages to requirements.txt)
5. **Use `.dockerignore`** to exclude unnecessary files from the image

---

## 🎯 Quick Command Reference

| Action | Command |
|--------|---------|
| **Build images** | `docker compose -f docker-compose.yml build` |
| **Start containers** | `docker compose -f docker-compose.yml up -d` |
| **Build + Start (shortcut)** | `docker compose up -d --build` |
| **Stop containers** | `docker compose down` |
| **View logs** | `docker compose logs -f` |
| **Run migrations** | `docker compose exec web python manage.py migrate` |
| **Access shell** | `docker compose exec web bash` |
| **Fresh start** | `docker compose down -v && docker compose up -d --build` |

---

## ✅ Verification

After starting the application, verify it's running:

```bash
# Check if containers are running
docker compose ps

# Test the API
curl http://localhost:8000/api/

# View logs
docker compose logs -f web
```

---

## 📝 Notes

- The application runs on `http://localhost:8000`
- The database runs on `localhost:5432` (if using PostgreSQL)
- Changes to Python code require a rebuild: `docker compose up -d --build`
- Changes to static files require: `docker compose exec web python manage.py collectstatic`

---

## 🤝 Contributing

1. Make your changes
2. Test locally with `docker compose up -d --build`
3. Run tests: `docker compose exec web python manage.py test`
4. Submit your pull request

