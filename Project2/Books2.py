# Import necessary FastAPI and Pydantic modules
from fastapi import FastAPI, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from starlette import status

print(">>> Project2/Books2.py LOADED")

# Create FastAPI application instance
app = FastAPI(title="📚 My Books API - Project 2")

# Define the Book model using Pydantic BaseModel
# This model validates and structures book data
class Book(BaseModel):
    id: Optional[int] = None  # ID is optional (auto-generated when creating)
    title: str = Field(min_length=3)  # Title must be at least 3 characters
    author: str = Field(min_length=3)  # Author must be at least 3 characters
    description: str = Field(min_length=3, max_length=100)  # Description between 3-100 characters
    rating: int = Field(ge=1, le=5)  # Rating must be between 1 and 5 (inclusive)
    published_date: int = Field(ge=1999, le=2031, description="Year when the book was published (1999-2031)")  # Published date must be between 1999 and 2031
    
    # Configuration for JSON schema (shows example in Swagger UI)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A classic American novel about the Jazz Age",
                "rating": 5,
                "published_date": 2012
            }
        }
    ) 

# Initialize the Books list with sample data
Books = [
    Book(id=1, title="The Great Gatsby", author="F. Scott Fitzgerald", description="A story about a man who is rich and wants to be happy", rating=2, published_date=2000),
    Book(id=2, title="To Kill a Mockingbird", author="Harper Lee", description="A story about a man who is rich and wants to be happy", rating=5, published_date=2005),
    Book(id=3, title="1984", author="George Orwell", description="A story about a man who is rich and wants to be happy", rating=3, published_date=2010),
    Book(id=4, title="Pride and Prejudice", author="Jane Austen", description="A story about a man who is rich and wants to be happy", rating=5, published_date=2015),
    Book(id=5, title="The Catcher in the Rye", author="J.D. Salinger", description="A story about a man who is rich and wants to be happy", rating=5, published_date=2020),
    Book(id=6, title="Sapiens", author="Yuval Noah Harari", description="A story about a man who is rich and wants to be happy", rating=3, published_date=2011)
]

# Root endpoint - returns welcome message
@app.get("/")
async def root():  
    return {"message": "Welcome to the Books API - Project 2. Try /books"}

# GET endpoint - returns all books in the list
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return Books

# POST endpoint - creates a new book
# Automatically assigns an ID if not provided
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: Book):
    updated_book = find_book_id(book_request)  # Auto-generate ID if missing
    Books.append(updated_book)  # Add the new book to the list
    return updated_book  # Return the created book

# Helper function to auto-generate book ID
# If Books list is empty, starts with ID 1
# Otherwise, uses the last book's ID + 1
def find_book_id(book: Book):
    book.id = 1 if len(Books) == 0 else Books[-1].id + 1
    return book

# GET endpoint - returns books filtered by rating
# Uses path parameter to get rating value (must be between 1-5)
@app.get("/books/by-rating/{rating}", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Path(ge=1, le=5, description="Rating value between 1 and 5")):
    # Filter books that match the requested rating
    books_to_return = [book for book in Books if book.rating == rating]
    # If no books found, return 404 error
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found with the given rating")
    return books_to_return

# GET endpoint - returns books filtered by published date (year)
# Uses path parameter to get the published year
@app.get("/books/by-published-date/{published_date}", status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int = Path(description="Year when the book was published")):
    # Filter books that match the requested published date
    books_to_return = [book for book in Books if book.published_date == published_date]
    # If no books found, return 404 error
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found with the given published date")
    return books_to_return


# GET endpoint - returns a single book by its ID
# Uses path parameter to get the book_id
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id: int = Path(gt=0, description="The ID of the book to get")):
    # Loop through all books to find the one with matching ID
    for book in Books:
        if book.id == book_id:
            return book  # Return the found book
    # If book not found, return 404 error
    raise HTTPException(status_code=404, detail="Book not found")

# PUT endpoint - updates an existing book by ID
# Takes book_id from path and updated book data from request body
@app.put("/books/update_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: int, book_update: Book):
    # Loop through books with index to update the correct one
    for i, book in enumerate(Books):
        if book.id == book_id:
            Books[i] = book_update  # Replace the old book with new data
            Books[i].id = book_id  # Ensure ID matches the path parameter
            return  # HTTP 204 No Content - no response body
    # If book not found, return 404 error
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE endpoint - removes a book by its ID
# Takes book_id from path parameter
@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int=Path(gt=0, description="The ID of the book to delete")):
    # Loop through books with index to find and remove the correct one
    for i, book in enumerate(Books):
        if book.id == book_id:
            Books.pop(i)  # Remove book from list
            return  # HTTP 204 No Content - no response body
    # If book not found, return 404 error
    raise HTTPException(status_code=404, detail="Book not found")
