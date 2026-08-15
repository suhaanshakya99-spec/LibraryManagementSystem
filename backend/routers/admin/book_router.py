from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from schemas.book_schemas import (BookResponse, CreateBook, UpdateBook)
from database.database import get_db
from services.book_services import (create_book,
                                    get_book_by_id,
                                    get_book_by_title,
                                    get_all_books,
                                    update_book,
                                    delete_book)
from dependency.admin_auth import requires_admin


router = APIRouter(prefix="/library/admin/book", tags=["books"], dependencies=[Depends(requires_admin)])

# creating a resource should return 201, not the default 200
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(data:CreateBook, db:Session= Depends(get_db)):
    new_book = create_book(data, db)
    return new_book

@router.get("/id/{id}", response_model=BookResponse)
def fetch_book_by_id(id:int, db:Session = Depends(get_db)):
    book = get_book_by_id(id, db)

    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    else:
        return book

@router.get("/title/{title}", response_model=BookResponse)
def fetch_book_by_title(title:str, db:Session= Depends(get_db)):
    book = get_book_by_title(title, db)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return book
    

@router.get("/books", response_model=list[BookResponse]) #list[BookResponse] -> type hint
def fetch_all_books(db:Session = Depends(get_db)):
    books = get_all_books(db)

    return books

@router.patch("/id/{id}", response_model=BookResponse)
def book_update(id:int, data:UpdateBook, db:Session=Depends(get_db)):

    updated_book = update_book(id, data, db)

    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return updated_book
    

@router.delete("/id/{id}")
def destroy_book(id:int, db:Session=Depends(get_db)):
    destroyed_book = delete_book(id, db)
    
    if destroyed_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return destroyed_book