# Todo App API

FastAPI-based Todo application with PostgreSQL, JWT authentication, and user management.

## Features

- User authentication (JWT tokens)
- Todo CRUD operations (user-scoped)
- Admin endpoints for managing all todos
- User profile management
- Password change and phone number update
- Database migrations with Alembic

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Create a `.env` file:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/database_name
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Start server:**
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

- **Auth**: `/auth/` (POST - create user), `/auth/token` (POST - login)
- **Users**: `/users/me` (GET), `/users/change-password` (PUT), `/users/phone-number` (PUT)
- **Todos**: `/todo` (GET, POST), `/todo/{id}` (GET, PUT, DELETE)
- **Admin**: `/admin/todos` (GET), `/admin/todos/{id}` (DELETE)

## Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

