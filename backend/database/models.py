from __future__ import annotations

from database.database import Base, engine
from sqlalchemy import Column, String, Integer, Date, ForeignKey, DateTime
from datetime import date, timedelta, datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Books(Base):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    status:Mapped[str] = mapped_column(String, default="Available")

    borrows:Mapped[list[Borrows]] = relationship("Borrows", back_populates="books")
    requests:Mapped[list[Requests]] = relationship("Requests", back_populates="book")
    


class Members(Base):

    __tablename__ = "members"

    id:Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name:Mapped[str] = mapped_column(String)
    email:Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    membership_date:Mapped[date] = mapped_column(Date, default= date.today) #Here is the function. Run it when needed.
    membership_expiry:Mapped[date] = mapped_column(Date, default= lambda: date.today() + timedelta(days=30))
    status:Mapped[str] = mapped_column(String, default="Active")
    is_verified:Mapped[bool] = mapped_column(default=False)

    borrows:Mapped[list[Borrows]]= relationship("Borrows", back_populates="members")
    requests:Mapped[list[Requests]] = relationship("Requests", back_populates="member")
    


class Borrows(Base):

    __tablename__ = "borrows"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    book_id:Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id:Mapped[int] = mapped_column(ForeignKey("members.id"))
    borrow_date:Mapped[date] = mapped_column(Date, default=date.today)
    due_date:Mapped[date] = mapped_column(Date, default= lambda:date.today() + timedelta(days=30))
    status:Mapped[str] = mapped_column(String, default="Borrowed")

    books:Mapped[Books] = relationship("Books", back_populates="borrows")
    members:Mapped[Members] = relationship("Members", back_populates="borrows")


class Requests(Base):

    __tablename__ = "requests"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_id:Mapped[int] = mapped_column(ForeignKey("books.id") ,index=True)
    member_id:Mapped[int] = mapped_column(ForeignKey("members.id") ,index=True)
    status:Mapped[str] = mapped_column(default="Pending")

    book:Mapped[Books] = relationship("Books", back_populates="requests")
    member:Mapped[Members] = relationship("Members", back_populates="requests")

    request_date:Mapped[date] = mapped_column(default=date.today)


class Tokens(Base):

    __tablename__ = "tokens"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    token:Mapped[str] = mapped_column(unique=True, index=True)
    token_type:Mapped[str] = mapped_column()
    expires_at:Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used:Mapped[bool] = mapped_column(default=False)

    member:Mapped[Members] = relationship("Members")




    
