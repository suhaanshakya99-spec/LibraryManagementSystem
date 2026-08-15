from services.book_services import get_all_books
from services.borrow_services import get_borrows_of_member
from schemas.book_schemas import BookResponse
from schemas.borrow_schemas import BorrowResponse
from schemas.request_schemas import (RequestResponse, CreateRequest)
from services.request_services import (view_member_requests, remove_requets, request_borrow, view_request)
from database.database import get_db
from dependency.auth import get_current_user
from database.models import Members
from services.email_services import verify_email


from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/library/member", tags=["MemberSide"])

# show the member every book in the catalog
@router.get("/books", response_model=list[BookResponse])
def fetch_all_books(db:Session=Depends(get_db), member:Members=Depends(get_current_user)):
    return get_all_books(db)

# create a borrow request
@router.post("/request", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(data:CreateRequest, db:Session=Depends(get_db), member:Members=Depends(get_current_user)):
    # force member_id to the logged-in user, don't trust the client-sent value
    data.member_id = member.id
    return request_borrow(data, db)

# view all of the current member's own requests
@router.get("/request/mine", response_model=list[RequestResponse])
def show_all_requests(member:Members=Depends(get_current_user), db:Session=Depends(get_db)):
    return view_member_requests(member.id, db)


# show the current member their own borrows
@router.get("/borrows/mine", response_model=list[BorrowResponse])
def fetch_borrows_of_member(member:Members=Depends(get_current_user), db:Session=Depends(get_db)):
    return get_borrows_of_member(member.id, db)

# cancel one of the current member's own pending requests
@router.delete("/requests/{id}")
def delete_request(id:int, member:Members=Depends(get_current_user), db:Session=Depends(get_db)):
    # look up by the real request id and check ownership before deleting
    request = view_request(id, db)
    if request is None or request.member_id != member.id:
        raise HTTPException(status_code=404, detail="Request not found")
    return remove_requets(id, db)

@router.post("/verify_email")
def email_verification(token:str, db:Session=Depends(get_db)):
    return verify_email(token, db)
