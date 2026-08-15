from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import Base, engine

from routers.admin.book_router import router as book_router
from routers.admin.admin_router import router as admin_router
from routers.admin.member_router import router as member_router
from routers.admin.borrow_router import router as borrow_router
from routers.member.member_login_router import router as member_login_router
from routers.admin.dashboard_router import router as dashboard_router
from routers.member.member_side_router import router as member_side_router

app = FastAPI(title="Library Management System")

# credentials=True + origins="*" is rejected by browsers, and we don't use cookies anyway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_router)
app.include_router(admin_router)
app.include_router(member_router)
app.include_router(borrow_router)
app.include_router(member_login_router)
app.include_router(dashboard_router)
app.include_router(member_side_router)

@app.get("/")
def root():
    return {"message":"library management system is working"}

Base.metadata.create_all(bind= engine)


