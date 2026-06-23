from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

book: str = ''

class Book(BaseModel):
    name: str

@app.get('/book')
def get_book_name():
    return {'result' : f'Любимая книга: {book}'}

@app.post('/book')
def change_book(payload: Book):
    global book
    book = payload.name
    return {'message' : 'Книга успешно изменена'}