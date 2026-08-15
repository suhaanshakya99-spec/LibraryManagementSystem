from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.models import (Books, Members, Borrows)
from database.database import get_db
from schemas.dashboard_schema import DashboardResponse
from dependency.admin_auth import requires_admin

'''
1 total books
2 total members
3 available books
4 borrowed books
5 recent borrows
'''

router = APIRouter(prefix="/library/admin/dashboard", tags=["dashboard"], dependencies=[Depends(requires_admin)])

@router.get("/", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
def get_dashboard(db:Session=Depends(get_db)):

    total_books = db.query(Books).count()
    total_members = db.query(Members).count()

    available_books = db.query(Books).filter(
        Books.status == "Available"
    ).count()

    borrowed_books = db.query(Books).filter(
        Books.status == "Borrowed"
    ).count()

    #.all() return a list based on borrow_date in desc order
    recent_borrows = db.query(Borrows).order_by(Borrows.borrow_date.desc()).limit(5).all()

    return {"total_books":total_books,
            "total_members":total_members,
            "available_books":available_books,
            "borrowed_books":borrowed_books,
            "recent_borrows":recent_borrows}