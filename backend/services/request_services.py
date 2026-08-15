from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.request_schemas import (CreateRequest, UpdateRequest)
from schemas.borrow_schemas import CreateBorrow
from database.models import Requests
from services.borrow_services import createborrow


#sending requets
def request_borrow(data:CreateRequest, db:Session):

    request = Requests(**data.model_dump())

    db.add(request)
    db.commit()
    db.refresh(request)

    return request

#view requests by id
def view_request(id:int, db:Session):
    return db.query(Requests).filter(Requests.id == id).first()

def view_member_requests(id:int, db:Session):
    return db.query(Requests).filter(Requests.member_id == id).all()


def view_all_requests(db:Session):
    return db.query(Requests).all()

def remove_requets(id:int, db:Session):

    request = view_request(id, db)

    if request is None:
        raise HTTPException(status_code=404, detail="request not found")

    db.delete(request)
    db.commit()

    return {"message":"request was deleted"}

def approve_request(id:int, data:UpdateRequest, db:Session,):

    request = view_request(id, db)

    if request is None:
        raise HTTPException(status_code=404, detail="request not found")

    old_status = request.status

    for key, value in data.model_dump(exclude_unset=True).items():

        setattr(request, key, value)

    if data.status == "Approved" and old_status != "Approved":
        print("REQUEST BOOK ID:", request.book_id)
        print("REQUEST MEMBER ID:", request.member_id)
        createborrow_data = CreateBorrow(book_id=request.book_id, member_id=request.member_id)
        createborrow(createborrow_data, db)

    db.commit()
    db.refresh(request)

    return request
