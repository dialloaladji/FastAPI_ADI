from fastapi import FastAPI
from database import engine, Base
import Models

app = FastAPI(title="📝 Todo App API")

# Create all database tables
Base.metadata.create_all(bind=engine)
