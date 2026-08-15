from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from database.database import get_db
from config import settings


admin_auth_schema = OAuth2PasswordBearer(tokenUrl="/library/admin/login/", scheme_name="Admin side")

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY

def requires_admin(token:str=Depends(admin_auth_schema)):

    try:
        decoded_jwt = jwt.decode(token, algorithms=[ALGORITHM], key=SECRET_KEY)

        # check token_type too, or a long-lived admin refresh token could be used as an access token
        if decoded_jwt.get("sub") != "admin" or decoded_jwt.get("token_type") != "admin_access_token":
            raise HTTPException(status_code=401, detail="Admin token required")

        return decoded_jwt

    except (InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid token")

    




