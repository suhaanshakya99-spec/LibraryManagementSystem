from pwdlib import PasswordHash
from fastapi import HTTPException, Depends
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from database.models import Members
from config import settings
from schemas.security_schemas import Payload_Data
from dependency.auth import auth_schema



ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


password = PasswordHash.recommended()


def hash_password(data:str):
    hashed_password = password.hash(data)
    return hashed_password

def verify_password(user_given_password:str, database_hashed_password:str):
    if password.verify(user_given_password, database_hashed_password):
        return True
    else:
        raise HTTPException(status_code=401, detail="Password is incorrect")



#JWT
def create_access_token(data:Payload_Data):

    to_encode = data.model_dump().copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":exp, "token_type":"access_token"})

    access_token = jwt.encode(algorithm=ALGORITHM, payload=to_encode, key=SECRET_KEY)

    return access_token


def create_refresh_token(data:Payload_Data):

    to_encode = data.model_dump().copy()
    exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":exp, "token_type":"refresh_token"})

    refresh_token = jwt.encode(algorithm=ALGORITHM, payload=to_encode, key=SECRET_KEY)

    return refresh_token


def verify_refresh_token(data:str, db:Session):

    try:

        decoded_data = jwt.decode(data, algorithms=[ALGORITHM], key=SECRET_KEY)

        if decoded_data.get("token_type") != "refresh_token":
            raise HTTPException(status_code=401, detail="Token type is not valid")

        member = db.query(Members).filter(Members.email == decoded_data["email"]).first()

        # without this check a deleted member would just get a 200 with null body
        if member is None:
            raise HTTPException(status_code=401, detail="Member not found")

        payload = Payload_Data(id=member.id, email=member.email)
        access_token = create_access_token(payload)
        return {"access_token":access_token, "token-type":"bearer"}


    except(InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid refresh token")


def create_admin_access_token():

    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    admin_payload = {"sub":"admin", "token_type":"admin_access_token", "exp":exp}

    admin_access_token = jwt.encode(payload=admin_payload, algorithm=ALGORITHM, key=SECRET_KEY)

    return admin_access_token

def create_admin_refresh_token():

    # was timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS) -- expired in 7 minutes, not 7 days
    exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    admin_payload = {"sub":"admin", "token_type":"admin_refresh_token", "exp":exp}

    admin_refresh_token = jwt.encode(payload=admin_payload, algorithm=ALGORITHM, key=SECRET_KEY)

    return admin_refresh_token

def verify_admin_refesh_token(token:str):

    try:
        decoded_data = jwt.decode(token, algorithms=[ALGORITHM], key=SECRET_KEY)

        if decoded_data is None:
            raise HTTPException(status_code=401, detail="Invalid Token")

        if decoded_data["token_type"] != "admin_refresh_token":
            raise HTTPException(status_code=401, detail="Invalid token type")

        access_token = create_admin_access_token()
        return {"admin_access_token":access_token, "token_type":"bearer"}

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
