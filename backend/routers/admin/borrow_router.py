from fastapi import APIRouter, Depends, status, HTTPException
from database.database import get_db
from sqlalchemy.orm import Session
from services.borrow_services import (createborrow,
                                       get_all_borrows,
                                         update_borrow,
                                           get_borrow_by_id,
                                             delete_borrow)
from schemas.borrow_schemas import CreateBorrow, BorrowResponse, UpdateBorrow
from schemas.request_schemas import (UpdateRequest, RequestResponse)
from services.request_services import (view_all_requests, approve_request, view_request)
from dependency.admin_auth import requires_admin

router = APIRouter(prefix="/library/admin/borrows", tags=["borrows"], dependencies=[Depends(requires_admin)])

@router.post("/", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
def declare_borrow(data:CreateBorrow, db:Session=Depends(get_db)):
    borrow = createborrow(data, db)
    db.commit()
    db.refresh(borrow)

    return borrow

@router.get("/", response_model= list[BorrowResponse])
def fetch_all_borrows(db:Session=Depends(get_db)):
    return get_all_borrows(db)

@router.patch("/id/{id}", response_model=BorrowResponse)
def patch_borrow(id:int, data:UpdateBorrow, db:Session=Depends(get_db)):
    return update_borrow(id, data, db)

@router.get("/id/{id}", response_model=BorrowResponse)
def fetch_borrow_by_id(id:int, db:Session=Depends(get_db)):
    borrow = get_borrow_by_id(id, db)
    # without this, a missing borrow returned None and crashed response validation (500)
    if borrow is None:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return borrow

@router.delete("/id/{id}")
def delete_entry(id:int, db:Session=Depends(get_db)):
    return delete_borrow(id, db)

@router.get("/requests", response_model=list[RequestResponse])
def get_all_requests(db:Session=Depends(get_db)):
    return view_all_requests(db)

# id is a query param here (e.g. ?id=3); response_model fixes a 500 from encoding the raw ORM object
@router.put("/requests", response_model=RequestResponse)
def update_request(id:int, data:UpdateRequest, db:Session=Depends(get_db)):
    return approve_request(id, data, db)

@router.get("/request/id/{id}", response_model=RequestResponse)
def get_request(id:int, db:Session=Depends(get_db)):
    request = view_request(id, db)
    # same 404 fix as fetch_borrow_by_id above
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request