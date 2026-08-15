from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
from datetime import date


class CreateBorrow(BaseModel):
    book_id: int
    member_id: int


# these must be defined before BorrowResponse or it crashes on import (NameError)
class MemberInfo(BaseModel):
    id: int
    name: str


class BookInfo(BaseModel):
    id: int
    title: str


class BorrowResponse(BaseModel):
    id: int
    books: BookInfo
    members: MemberInfo

    borrow_date: date
    due_date: date

    status: Literal["Borrowed", "Returned", "Overdue"]

    model_config = ConfigDict(from_attributes=True)


class UpdateBorrow(BaseModel):
    id: Optional[int] = None
    book_id: Optional[int] = None
    member_id: Optional[int] = None

    borrow_date: Optional[date] = None
    due_date: Optional[date] = None

    status: Optional[Literal["Borrowed", "Returned", "Overdue"]] = None
