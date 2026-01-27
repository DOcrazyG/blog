# Blog API

A personal blog backend API built with FastAPI and PostgreSQL.

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Development Environment

Start the development environment with hot-reloading and exposed ports:

```bash
docker compose -f docker-compose-production.yml up --build
```

### Production Environment

Start the production environment with optimized settings:

```bash
docker compose -f docker-compose-production.yml up --build -d   
```

### Environment Variables

The application uses the following environment variables:

- `DATABASE_URL`: PostgreSQL database connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `ALGORITHM`: Algorithm for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Expiration time for access tokens
- `APP_NAME`: Application name
- `DEBUG`: Debug mode (True/False)

### API Endpoints

- `/`: Root endpoint
- `/health`: Health check endpoint
- `/api/auth`: Authentication endpoints
- `/api/users`: User management endpoints
- `/api/posts`: Blog post endpoints
- `/api/comments`: Comment endpoints
- `/api/tags`: Tag endpoints
