from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from database.database import get_db
from database.models import Members
from config import settings
from database.models import Members


auth_schema = OAuth2PasswordBearer(tokenUrl="/library/member/login", scheme_name="Member side")


ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY


def get_current_user(token:str=Depends(auth_schema), db:Session=Depends(get_db)):

    try:
        decoded_data = jwt.decode(token, algorithms=[ALGORITHM], key=SECRET_KEY)

        # without this check a refresh token could be reused as an access token
        if decoded_data.get("token_type") != "access_token":
            raise HTTPException(status_code=401, detail="Invalid token")

        member_email = decoded_data.get("email")
        member = db.query(Members).filter(Members.email == member_email).first()

        if member is None:
            raise HTTPException(status_code=404, detail="Member not found in database")

        return member
        
    except (InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid token")
        
  


    




