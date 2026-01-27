# Blog API

A personal blog backend API built with FastAPI and PostgreSQL.

## Features

- User management (registration, login, JWT authentication)
- Article management (CRUD operations)
- Comment system
- Tag categorization
- Article search
- RESTful API design
- Automatic API documentation (Swagger UI and ReDoc)
- Data validation
- Error handling and logging
- Unit tests and integration tests

## Tech Stack

- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT
- Uvicorn
- UV (for dependency management)

## Environment Requirements

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher
- UV (for dependency management)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd blog
```

### 2. Install dependencies using UV

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root directory:

```env
# Database connection string
DATABASE_URL="postgresql://admin:password@localhost:5432/example_db"

# Secret key for JWT tokens
SECRET_KEY="your-secret-key-here"

# Algorithm for JWT
ALGORITHM="HS256"

# Token expiration time (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application name
APP_NAME="Blog API"

# Debug mode
DEBUG=True
```

### 4. Create database tables

```bash
python -c "from app.utils.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

## Running the Application

### Development mode

```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Production mode

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

FastAPI automatically generates API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login with username and password
- `POST /api/auth/login/json` - Login with JSON format

### Users
- `GET /api/users/me` - Get current user information
- `PUT /api/users/me` - Update current user information
- `GET /api/users/{user_id}` - Get user information by ID

### Posts
- `POST /api/posts/` - Create a new post
- `GET /api/posts/` - Get post list with pagination, filtering, and search
- `GET /api/posts/me` - Get current user's posts
- `GET /api/posts/{post_id}` - Get post by ID
- `PUT /api/posts/{post_id}` - Update post by ID
- `DELETE /api/posts/{post_id}` - Delete post by ID

### Comments
- `POST /api/comments/` - Create a new comment
- `GET /api/comments/post/{post_id}` - Get comments for a post
- `PUT /api/comments/{comment_id}` - Update comment by ID
- `DELETE /api/comments/{comment_id}` - Delete comment by ID

### Tags
- `POST /api/tags/` - Create a new tag (admin only)
- `GET /api/tags/` - Get tag list
- `GET /api/tags/{tag_id}` - Get tag by ID
- `PUT /api/tags/{tag_id}` - Update tag by ID (admin only)
- `DELETE /api/tags/{tag_id}` - Delete tag by ID (admin only)

## Testing

Run the tests:

```bash
uv run pytest tests/
```

## Security

- JWT authentication
- Password hashing with bcrypt
- Input validation
- SQL injection protection (using SQLAlchemy ORM)
- CSRF protection
- XSS protection

## Deployment

### Using Docker Compose

The project includes a `docker-compose.yml` file for easy deployment with PostgreSQL.

#### 1. Build and start the containers

```bash
docker-compose up --build
```

#### 2. Access the API

The API will be available at `http://localhost:8000`.

#### 3. Stop the containers

```bash
docker-compose down
```

#### 4. Stop and remove volumes

```bash
docker-compose down -v
```

### Using Docker (Single Container)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9

WORKDIR /app

COPY pyproject.toml .
COPY .env .
COPY main.py .
COPY app/ app/

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run the Docker container:

```bash
docker build -t blog-api .
docker run -p 8000:8000 blog-api
```

### Using a process manager (e.g., Gunicorn)

```bash
uv run gunicorn -k uvicorn.workers.UvicornWorker main:app
```

## License

MIT
