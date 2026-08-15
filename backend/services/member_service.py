from schemas.member_schemas import (CreateMember, UpdateMember, MemberLogin)
from sqlalchemy.orm import Session
from database.models import Members, Tokens
from fastapi import HTTPException, BackgroundTasks
from datetime import date
from fastapi.security import OAuth2PasswordRequestForm
import secrets
from datetime import datetime, timezone, timedelta

from auth.security import (hash_password, verify_password, create_access_token, create_refresh_token)
from schemas.security_schemas import Payload_Data
from services.email_services import send_verification_mail
from config import settings


def create_member(data:CreateMember, db:Session, background:BackgroundTasks):

    hashed_password = hash_password(data.password)
    new_member = Members(name=data.name, email=data.email, hashed_password=hashed_password)

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    raw_token = secrets.token_urlsafe()
    to_email = new_member.email

    token = Tokens(
        user_id=new_member.id,
        token=raw_token,
        token_type= "email_verification_token",
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    )

    db.add(token)
    db.commit()

    # points at the actual frontend page, not an API route
    frontend_url = f"{settings.FRONTEND_URL}/member/verify-email.html?token={raw_token}"
    html = f"""
        <h2>Verify your email</h2>

        <p>
        Thank you for registering.
        Please click the button below to verify your email.
        </p>

        <a href="{frontend_url}">
            Verify Email
        </a>

        <p>This link expires in 24 hours.</p>
        """   

    background.add_task(send_verification_mail, subject="Email Verification", html=html, to_mail=to_email)

    return {"member":new_member, "verification_token":raw_token}

def get_all_memebers(db:Session):
    members = db.query(Members).all()

    for member in members:
        update_member_status(member=member, db=db)

    return members

def get_member_by_name(name:str, db:Session):
    member = db.query(Members).filter(Members.name == name).first()

    if member:
        return member
    else:
        raise HTTPException(status_code=404, detail="member not found")

def get_member_by_id(id:int, db:Session):

    member = db.query(Members).filter(Members.id == id).first()

    if member:
        return member
    else:
        raise HTTPException(status_code=404, detail="member not found")

def update_member(id:int, data:UpdateMember, db:Session):
    member = get_member_by_id(id, db)

    for key, value in data.model_dump(exclude_unset=True).items():
        # column is "hashed_password", not "password" -- hash it instead of setattr
        if key == "password":
            member.hashed_password = hash_password(value)
        else:
            setattr(member, key, value)

    db.commit()
    db.refresh(member)

    return member

def delete_member(id:int, db:Session):
    member = get_member_by_id(id, db)

    db.delete(member)
    db.commit()

    return {"message":"deleted successfully"}

def update_member_status(member:Members, db:Session):
    today = date.today()

    if member.membership_expiry < today:
        member.status = "Inactive"
        db.commit()
        db.refresh(member)

def get_member_by_email(email:str, db:Session):
    member = db.query(Members).filter(Members.email == email).first()
    return member

def member_login(data, db):

    member = get_member_by_email(data.username, db)

    if member is None:
        # 401 with a generic message -- 404 here would leak which emails are registered
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if verify_password(data.password, member.hashed_password):

        payload = Payload_Data(email=member.email, id=member.id)

        access_token = create_access_token(data=payload)
        refresh_token = create_refresh_token(data=payload)

        return {"access_token":access_token,
                "refresh_token":refresh_token,
                "token_type":"bearer"}

    

    
