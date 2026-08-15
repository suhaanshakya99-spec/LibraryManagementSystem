from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal

class BookResponse(BaseModel):
    id: int
    title:str
    author:str
    category:str
    status: Literal["Borrowed", "Available"]

    model_config = ConfigDict(from_attributes=True)

class CreateBook(BaseModel):
    title:str
    author:str
    category:str


class UpdateBook(BaseModel):
    title:Optional[str] = None
    author:Optional[str] = None
    category:Optional[str] = None
    status: Optional[Literal["Borrowed", "Available"]] = None

