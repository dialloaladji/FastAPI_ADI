from fastapi import Body, FastAPI, HTTPException

print(">>> Project1/Books.py LOADED")

app = FastAPI(title="📚 My Books API")

Books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "Category": "Fiction"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "Category": "Fiction"},
    {"title": "1984", "author": "George Orwell", "Category": "Dystopian Fiction"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "Category": "Romance"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "Category": "Fiction"},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "Category": "Non-Fiction"},
]

@app.get("/books")
async def read_all_books():
    return Books

@app.get("/")
async def root():
    return {"message": "Welcome to the Books API. Try /books"}

@app.get("/books/mybook")
async def my_favorite_book():
    return {"book_title": "My favorite book"}

@app.get("/books/category/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in Books:
        if book.get("Category").casefold() == category.casefold():
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Category not found")
    return books_to_return

@app.get("/books/by-author/")
async def get_books_by_author(author: str):
    books_to_return = []
    for book in Books:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Author not found")
    return books_to_return

@app.get("/books/by-author/{author_name}")
async def get_books_by_author_path(author_name: str):
    books_to_return = []
    for book in Books:
        if book.get("author").casefold() == author_name.casefold():
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Author not found")
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book: dict):
    Books.append(new_book)
    return new_book

@app.put("/books/update_book")
async def update_book(updated_book: dict):
    for i, book in enumerate(Books):
        if book.get("title").casefold() == updated_book.get("title").casefold():
            Books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_title}")
async def delete_book(book_title: str):
    for i, book in enumerate(Books):
        if book.get("title").casefold() == book_title.casefold():
            deleted_book = Books.pop(i)
            return deleted_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/{book_author}/")
async def read_author_category_by_query(author: str = None, category: str = None):
    books_to_return = []
    for book in Books:
        if (not author or book.get("author").casefold() == author.casefold()) and \
           (not category or book.get("Category").casefold() == category.casefold()):
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found")
    return books_to_return
# @app.get("/books/{book_title}")
# async def read_book(book_title: str):
#     for book in Books:
#         if book.get("title").casefold() == book_title.casefold():
#             return book
#     raise HTTPException(status_code=404, detail="Book not found")


