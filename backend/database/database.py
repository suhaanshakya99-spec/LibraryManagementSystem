from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

#creating engine
URL = settings.DATABASE_URL
engine = create_engine(URL, connect_args={"check_same_thread":False})

#creating a parent base
class Base(DeclarativeBase):
    pass

#creating session factory 
LocalSession = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

    
