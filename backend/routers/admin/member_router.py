from fastapi import APIRouter, Depends, BackgroundTasks, status
from schemas.member_schemas import (CreateMember, UpdateMember, MemberDetail, MemberRegisterResponse)
from services.member_service import (create_member,
                                    get_all_memebers, 
                                    get_member_by_id,
                                    update_member,
                                    delete_member,
                                    get_member_by_name
                                    )
from database.database import get_db
from sqlalchemy.orm import Session
from dependency.admin_auth import requires_admin
from services.email_services import verify_email


router = APIRouter(prefix="/library/admin/members", tags=["members"], dependencies=[Depends(requires_admin)])

# creating a resource should return 201, not the default 200
@router.post("/", response_model=MemberRegisterResponse, status_code=status.HTTP_201_CREATED)
def add_member(data:CreateMember, background:BackgroundTasks, db:Session= Depends(get_db)):
    return create_member(data, db, background)

# these used to use MemberResponse (the login/token schema) and crashed with a 500
@router.get("/id/{id}", response_model=MemberDetail)
def fetch_member_by_id(id:int, db:Session= Depends(get_db)):
    return get_member_by_id(id, db)

@router.get("/name/{name}", response_model=MemberDetail)
def fetch_member_by_name(name:str, db:Session= Depends(get_db)):
    return get_member_by_name(name, db)

@router.get("/", response_model=list[MemberDetail])
def fetch_all_memebers(db:Session= Depends(get_db)):
    return get_all_memebers(db)

@router.patch("/id/{id}", response_model=MemberDetail)
def member_update(id:int, data:UpdateMember, db:Session= Depends(get_db)):
    return update_member(id, data, db)

@router.delete("/id/{id}")
def destroy_member(id:int, db:Session= Depends(get_db)):
    return delete_member(id, db)
