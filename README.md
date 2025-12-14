# FastAPI Training Projects

A collection of FastAPI training projects demonstrating RESTful API development, data validation, database integration, and best practices.

## 📚 Table of Contents

- [Overview](#overview)
- [Projects](#projects)
  - [Project1: Books API (Basic)](#project1-books-api-basic)
  - [Project2: Books API (Advanced)](#project2-books-api-advanced)
  - [TodoApp: Todo Management API](#todoapp-todo-management-api)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## Overview

This repository contains three progressive FastAPI projects designed to teach and demonstrate:

- **Project1**: Basic FastAPI concepts with in-memory data storage
- **Project2**: Advanced FastAPI with Pydantic validation and data modeling
- **TodoApp**: Full-stack application with SQLAlchemy ORM and SQLite database

## Projects

### Project1: Books API (Basic)

A simple FastAPI application demonstrating basic REST API concepts with in-memory data storage.

**Features:**
- GET endpoints for retrieving books
- Filtering by category and author
- POST, PUT, DELETE operations
- In-memory data storage (dictionary-based)

**Key Concepts:**
- FastAPI route decorators
- HTTP methods (GET, POST, PUT, DELETE)
- Query parameters and path parameters
- HTTP status codes

**Run the application:**
```bash
cd Project1
uvicorn Books:app --reload --port 8000
```

**API Endpoints:**
- `GET /` - Welcome message
- `GET /books` - Get all books
- `GET /books/favorite` - Get favorite book
- `GET /books/by-category/{category}` - Filter by category
- `GET /books/by-author/{author}` - Filter by author
- `POST /books` - Create a new book
- `PUT /books` - Update a book
- `DELETE /books/{book_title}` - Delete a book by title

### Project2: Books API (Advanced)

An enhanced FastAPI application with Pydantic models, data validation, and auto-incrementing IDs.

**Features:**
- Pydantic BaseModel for data validation
- Field validation (min_length, max_length, ge, le)
- Auto-incrementing book IDs
- Filtering by rating and published date
- Swagger UI examples via ConfigDict

**Key Concepts:**
- Pydantic models and validation
- Field constraints and validation
- Path and Query parameters
- HTTP status codes (200, 201, 204, 404)
- Model configuration for API documentation

**Run the application:**
```bash
cd Project2
uvicorn Books2:app --reload --port 8001
```

**API Endpoints:**
- `GET /` - Get all books
- `GET /books/by-rating/{rating}` - Filter by rating (1-5)
- `GET /books/by-published-date/{published_date}` - Filter by year
- `GET /books/{book_id}` - Get book by ID
- `POST /create-book` - Create a new book (auto-generates ID)
- `PUT /books/update_book/{book_id}` - Update book by ID
- `DELETE /books/delete_book/{book_id}` - Delete book by ID

**Book Model:**
```python
{
    "id": int (optional, auto-generated),
    "title": str (min 3 chars),
    "author": str (min 3 chars),
    "description": str (3-100 chars),
    "rating": int (1-5),
    "published_date": int (1999-2031)
}
```

### TodoApp: Todo Management API

A complete FastAPI application with SQLAlchemy ORM, SQLite database, and comprehensive CRUD operations.

**Features:**
- SQLAlchemy ORM for database operations
- SQLite database with automatic table creation
- Full CRUD operations (Create, Read, Update, Delete)
- Pydantic models for request validation
- Dependency injection for database sessions
- Comprehensive error handling

**Key Concepts:**
- SQLAlchemy ORM models
- Database session management
- Dependency injection with FastAPI
- Database migrations and table creation
- Transaction management (commit, rollback)

**Run the application:**
```bash
cd TodoApp
uvicorn main:app --reload --port 8002
```

**API Endpoints:**
- `GET /` - Get all todos
- `GET /todo/{todo_id}` - Get todo by ID
- `POST /todo` - Create a new todo
- `PUT /todo/{todo_id}` - Update todo by ID
- `DELETE /todo/{todo_id}` - Delete todo by ID

**Todo Model:**
```python
{
    "id": int (auto-generated primary key),
    "title": str (min 3 chars),
    "description": str (3-100 chars),
    "priority": int (1-6),
    "complete": bool (default: false)
}
```

**Database:**
- SQLite database file: `todos.db`
- Tables are automatically created on application startup
- Database file is excluded from Git (see `.gitignore`)

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.9+**: Programming language
- **Pydantic**: Data validation using Python type annotations
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **SQLite**: Lightweight, file-based database
- **Uvicorn**: ASGI server for running FastAPI applications

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/dialloaladji/FastAPI_ADI.git
cd FastAPItraining
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv fasteapi_env
source fasteapi_env/bin/activate  # On Windows: fasteapi_env\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

Or install from requirements file (if available):
```bash
pip install -r requirements.txt
```

## Usage

### Running Project1

```bash
cd Project1
uvicorn Books:app --reload --port 8000
```

Access the API at: `http://127.0.0.1:8000`
Swagger UI: `http://127.0.0.1:8000/docs`

### Running Project2

```bash
cd Project2
uvicorn Books2:app --reload --port 8001
```

Access the API at: `http://127.0.0.1:8001`
Swagger UI: `http://127.0.0.1:8001/docs`

### Running TodoApp

```bash
cd TodoApp
uvicorn main:app --reload --port 8002
```

Access the API at: `http://127.0.0.1:8002`
Swagger UI: `http://127.0.0.1:8002/docs`

**Note:** The database file (`todos.db`) will be automatically created in the `TodoApp` directory on first run.

## Project Structure

```
FastAPItraining/
├── Project1/
│   ├── Books.py              # Main FastAPI application
│   ├── __init__.py           # Package initialization
│   └── test_api.py           # API testing utilities
├── Project2/
│   ├── Books2.py             # Advanced FastAPI application with Pydantic
│   └── __init__.py           # Package initialization
├── TodoApp/
│   ├── main.py               # FastAPI application with database
│   ├── Models.py             # SQLAlchemy ORM models
│   ├── database.py           # Database configuration
│   ├── Todos.py              # Additional todo utilities
│   ├── check_db.py           # Database configuration checker
│   ├── __init__.py           # Package initialization
│   └── todos.db              # SQLite database (auto-generated, git-ignored)
├── .gitignore                # Git ignore rules
└── README.md                  # This file
```

## API Documentation

All projects include automatic interactive API documentation via Swagger UI:

- **Swagger UI**: Available at `/docs` endpoint (e.g., `http://127.0.0.1:8000/docs`)
- **ReDoc**: Available at `/redoc` endpoint (e.g., `http://127.0.0.1:8000/redoc`)
- **OpenAPI Schema**: Available at `/openapi.json` endpoint

### Example API Calls

**Create a Todo (TodoApp):**
```bash
curl -X POST "http://127.0.0.1:8002/todo" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "priority": 5,
    "complete": false
  }'
```

**Get All Books (Project1):**
```bash
curl http://127.0.0.1:8000/books
```

**Create a Book (Project2):**
```bash
curl -X POST "http://127.0.0.1:8001/create-book" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "description": "A classic American novel",
    "rating": 5,
    "published_date": 1925
  }'
```

## Contributing

This is a training repository. Feel free to:
- Fork the repository
- Create feature branches
- Submit pull requests
- Report issues

## License

This project is for educational purposes.

## Author

**Diallo Aladji**
- Email: dialloalgass90@gmail.com
- GitHub: [@dialloaladji](https://github.com/dialloaladji)

## Acknowledgments

- FastAPI documentation and community
- SQLAlchemy documentation
- Pydantic documentation

---

**Happy Coding! 🚀**
