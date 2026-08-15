from sqlalchemy.orm import Session
from schemas.book_schemas import (CreateBook, UpdateBook)
from database.models import Books

def create_book(data:CreateBook, db:Session):
    new_book = Books(**data.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return new_book

def get_book_by_id(id:int, db:Session):
    book = db.query(Books).filter(Books.id == id).first()
    if not book:
        return None
    else:
        return book
    
def get_book_by_title(title:str, db:Session):
    book = db.query(Books).filter(Books.title == title).first()
    if not book:
        return None
    else:
        return book
    
def update_book(id:int, data:UpdateBook, db:Session):
    book = get_book_by_id(id, db)

    if book is None:
        return None
    else:
        for key, value in data.model_dump(exclude_unset=True).items():
        #only client sent data is used
            setattr(book, key, value)
        
        db.commit()
        db.refresh(book)

        return book
    
def get_all_books(db:Session):
    return db.query(Books).all()

def delete_book(id:int, db:Session):
    book = get_book_by_id(id, db)

    if book:
        db.delete(book)
        db.commit()
        return {"message":"book was deleted"}
    else:
        return None

    