from schemas.borrow_schemas import CreateBorrow, UpdateBorrow
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from database.models import Borrows, Books, Members

from datetime import date

def createborrow(data:CreateBorrow, db:Session):

    book = db.get(Books, data.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    if book.status == "Borrowed":
        raise HTTPException(status_code=400, detail="book already borrowed")

    member = db.get(Members, data.member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="member not found")

    new_borrow = Borrows(**data.model_dump())

    book.status = 'Borrowed'
 
    db.add(new_borrow)

    return new_borrow

def get_all_borrows(db: Session):
    all_borrows = db.query(Borrows).all()

    for borrow in all_borrows:
        update_borrow_status(borrow)

    return all_borrows


def get_borrow_by_id(id:int, db:Session):
    borrow = db.get(Borrows, id)
    return borrow


def update_borrow(id:int, data:UpdateBorrow, db:Session):

    borrow = get_borrow_by_id(id, db)

    if not borrow:
        raise HTTPException(status_code= 404, detail="borrow does not exist")

    if data.status == "Returned":
        book = db.get(Books, borrow.book_id)

        if book is not None:
            book.status = "Available"


    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(borrow, key, value)


    db.commit()
    db.refresh(borrow)
    return borrow

def delete_borrow(id:int, db:Session):
    borrow = get_borrow_by_id(id, db)
    
    if borrow is None:
        raise HTTPException(status_code= 404, detail="borrow does not exist")

    if borrow is not None:
        borrow.books.status = "Available"


    db.delete(borrow)
    db.commit()

    return {"message":"data has been deleted"}

def get_borrows_of_member(id:int, db:Session):
    member_borrows = db.query(Borrows).filter(Borrows.member_id == id).all()
    return member_borrows

#updates the borrow status tp Overdue
def update_borrow_status(borrow:Borrows):

    if borrow.due_date < date.today():
        borrow.status = "Overdue"
    

