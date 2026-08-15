from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
from datetime import date


class CreateRequest(BaseModel):
    book_id: int
    member_id: int


# must be defined before RequestResponse or it crashes on import (NameError)
class BookInfo(BaseModel):
    id: int
    title: str


class MemberInfo(BaseModel):
    id: int
    name: str


class RequestResponse(BaseModel):
    id: int
    book_id: int
    member_id: int

    book: BookInfo
    member: MemberInfo

    request_date: date
    status: Literal["Pending", "Approved", "Reject"]

    model_config = ConfigDict(from_attributes=True)


class UpdateRequest(BaseModel):
    status: Optional[Literal["Approved", "Pending", "Reject"]] = None
