from fastapi import APIRouter, HTTPException, Depends
from schemas.admin_schemas import AdminPasswordVerification
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from auth.security import (create_admin_access_token, create_admin_refresh_token, verify_admin_refesh_token)

router = APIRouter(prefix="/library/admin/login", tags=["admin"])

admin_name = settings.ADMIN_NAME
admin_password = settings.ADMIN_PASSWORD

@router.post("/")
def verfiy_admin(data:OAuth2PasswordRequestForm=Depends()):
    if data.username == admin_name and data.password == admin_password:
        access_token = create_admin_access_token()
        refresh_token = create_admin_refresh_token()

        return {"access_token":access_token,
                "refresh_token":refresh_token,
                "token_type":"bearer"}
    else:
        # wrong credentials is 401, not 400 -- the request itself was fine
        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/verify_refresh_token")
def resend_admin_access_token(token:str):
    return verify_admin_refesh_token(token)


