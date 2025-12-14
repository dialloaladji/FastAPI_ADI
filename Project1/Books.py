# Import FastAPI modules for creating the API, handling HTTP exceptions, and request body parsing
from fastapi import Body, FastAPI, HTTPException

print(">>> Project1/Books.py LOADED")

# Create FastAPI application instance
app = FastAPI(title="📚 My Books API")

# Initialize the Books list with sample data (dictionary format)
# Each book has title, author, and Category fields
Books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "Category": "Fiction"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "Category": "Fiction"},
    {"title": "1984", "author": "George Orwell", "Category": "Dystopian Fiction"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "Category": "Romance"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "Category": "Fiction"},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "Category": "Non-Fiction"},
]

# GET endpoint - returns all books in the list
@app.get("/books")
async def read_all_books():
    return Books

# GET endpoint - root endpoint that returns a welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to the Books API. Try /books"}

# GET endpoint - returns a hardcoded favorite book message
@app.get("/books/mybook")
async def my_favorite_book():
    return {"book_title": "My favorite book"}

# GET endpoint - filters books by category using query parameter
# Example: /books/category/?category=Fiction
@app.get("/books/category/")
async def read_category_by_query(category: str):
    books_to_return = []
    # Loop through all books and find matches (case-insensitive comparison)
    for book in Books:
        if book.get("Category").casefold() == category.casefold():
            books_to_return.append(book)
    # If no books found, return 404 error
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Category not found")
    return books_to_return

# GET endpoint - filters books by author using query parameter
# Example: /books/by-author/?author=George Orwell
@app.get("/books/by-author/")
async def get_books_by_author(author: str):
    books_to_return = []
    # Loop through all books and find matches (case-insensitive comparison)
    for book in Books:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    # If no books found, return 404 error
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Author not found")
    return books_to_return

# GET endpoint - filters books by author using path parameter
# Example: /books/by-author/George Orwell
@app.get("/books/by-author/{author_name}")
async def get_books_by_author_path(author_name: str):
    books_to_return = []
    # Loop through all books and find matches (case-insensitive comparison)
    for book in Books:
        if book.get("author").casefold() == author_name.casefold():
            books_to_return.append(book)
    # If no books found, return 404 error
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Author not found")
    return books_to_return

# POST endpoint - creates a new book
# Takes a dictionary with book data in the request body
@app.post("/books/create_book")
async def create_book(new_book: dict):
    Books.append(new_book)  # Add the new book to the list
    return new_book  # Return the created book

# PUT endpoint - updates an existing book by matching title
# Finds the book by title (case-insensitive) and replaces it with updated data
@app.put("/books/update_book")
async def update_book(updated_book: dict):
    # Loop through books with index to update the correct one
    for i, book in enumerate(Books):
        if book.get("title").casefold() == updated_book.get("title").casefold():
            Books[i] = updated_book  # Replace the old book with new data
            return updated_book  # Return the updated book
    # If book not found, return 404 error
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE endpoint - removes a book by its title
# Uses path parameter to get the book title
@app.delete("/books/{book_title}")
async def delete_book(book_title: str):
    # Loop through books with index to find and remove the correct one
    for i, book in enumerate(Books):
        if book.get("title").casefold() == book_title.casefold():
            deleted_book = Books.pop(i)  # Remove book from list and store it
            return deleted_book  # Return the deleted book
    # If book not found, return 404 error
    raise HTTPException(status_code=404, detail="Book not found")

# GET endpoint - filters books by author and/or category using query parameters
# Both parameters are optional - can filter by author only, category only, or both
# Example: /books/George Orwell/?category=Fiction
@app.get("/books/{book_author}/")
async def read_author_category_by_query(author: str = None, category: str = None):
    books_to_return = []
    # Loop through all books and apply filters
    for book in Books:
        # Check if book matches author filter (if provided) AND category filter (if provided)
        if (not author or book.get("author").casefold() == author.casefold()) and \
           (not category or book.get("Category").casefold() == category.casefold()):
            books_to_return.append(book)
    # If no books found, return 404 error
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found")
    return books_to_return
