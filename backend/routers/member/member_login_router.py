from schemas.member_schemas import MemberLogin, MemberResponse
from services.member_service import member_login
from database.database import get_db
from auth.security import verify_refresh_token


from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/library/member/login", tags=["member"])

@router.post("/", response_model= MemberResponse)
def login_attempt(data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    return member_login(data, db)

@router.post("/refresh_token_verify")
def resend_access_token(data:str, db:Session=Depends(get_db)):
    return verify_refresh_token(data, db)