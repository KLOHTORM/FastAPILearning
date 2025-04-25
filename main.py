from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 0, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Мистика", "pages": 448},
    {"id": 1, "title": "Война и мир", "author": "Лев Толстой", "genre": "Роман", "pages": 1274},
    {"id": 2, "title": "Убить пересмешника", "author": "Харпер Ли", "genre": "Классическая литература", "pages": 448},
    {"id": 3, "title": "Гарри Поттер и философский камень", "author": "Джоан Роулинг", "genre": "Фэнтези", "pages": 223},
    {"id": 4, "title": "Алхимик", "author": "Пауло Коэльо", "genre": "Философская проза", "pages": 208}
]

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    pages: int

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/books")
def get_books():
    return books

@app.get("/books/{id}")
def get_book_by_id(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

@app.delete("/books/{id}")
def delete_book_by_id(id: int):
    for book in books:
        if book["id"] == id:
            books.remove(book)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(new_book: BookCreate):
    new_id = max([book["id"] for book in books], default=0) + 1
    book_to_add = {
        "id": new_id,
        "title":new_book.title,
        "author": new_book.author,
        "pages": new_book.pages,
    }
    books.append(book_to_add)
    return book_to_add

@app.put("/books/{id}", status_code=status.HTTP_200_OK)
def update_book(id: int, updated_book: BookCreate):
    for book in books:
        if book["id"] == id:
            book["title"] = updated_book.title
            book["author"] = updated_book.author
            book["genre"] = updated_book.genre
            book["pages"] = updated_book.pages
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")


