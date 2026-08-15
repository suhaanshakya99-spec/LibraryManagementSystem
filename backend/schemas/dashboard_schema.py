from pydantic import BaseModel
from schemas.borrow_schemas import BorrowResponse

class DashboardResponse(BaseModel):
    total_books:int
    total_members:int
    available_books:int
    borrowed_books:int
    recent_borrows:list[BorrowResponse]

