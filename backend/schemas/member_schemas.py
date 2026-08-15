from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Literal
from datetime import date

class CreateMember(BaseModel):
    name: str
    email: EmailStr
    password: str

class UpdateMember(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    membership_date: Optional[date] = None
    membership_expiry: Optional[date] = None
    status: Optional[Literal["Active", "Inactive"]] = None

# login response only, not for returning member records (use MemberDetail for that)
class MemberResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str

    model_config = ConfigDict({"from_attributes":True})

class MemberPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class MemberDetail(BaseModel):
    id: int
    name: str
    email: EmailStr
    membership_date: date
    membership_expiry: date
    status: Literal["Active", "Inactive"]
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)

class MemberRegisterResponse(BaseModel):
    member:MemberPublic
    verification_token:str

class MemberLogin(BaseModel):
    email: EmailStr
    password: str