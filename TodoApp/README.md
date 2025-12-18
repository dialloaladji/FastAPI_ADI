# Todo App API

FastAPI Todo application with PostgreSQL, JWT authentication, and user management.

## Quick Start

1. Create `.env` file:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/database_name
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

3. Start server:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
