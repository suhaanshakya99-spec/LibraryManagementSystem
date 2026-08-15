import resend 
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta

from config import settings
from database.models import Tokens, Members

API_KEY = settings.RESEND_API
FROM_EMAIL = settings.FROM_EMAIL

resend.api_key = API_KEY

def send_verification_mail(to_mail:str, subject:str, html:str):

    params:resend.Emails.SendParams = {
        "from":FROM_EMAIL,
        "to":[to_mail],
        "subject":subject,
        "html":html
    }

    resend.Emails.send(params)


def verify_email(token:str, db:Session):

    db_token = db.query(Tokens).filter(Tokens.token == token, Tokens.token_type == "email_verification_token").first()

    if db_token is None:
        raise HTTPException(status_code=401, detail="Token is not valid")

    if db_token.expires_at <= datetime.now(timezone.utc).replace(tzinfo=None):
        raise HTTPException(status_code=401, detail="Token has expired")

    if db_token.used:
        raise HTTPException(status_code=401, detail="Token already used")

    member = db.query(Members).filter(Members.id == db_token.user_id).first()

    if member is None:
        raise HTTPException(status_code=404, detail="Member not found in database")

    try:
        member.is_verified = True
        db_token.used = True
        db.commit()
    except Exception:
        db.rollback()
        raise


    return {"message":"Your account has been verified"}


