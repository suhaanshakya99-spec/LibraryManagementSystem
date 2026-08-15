from pydantic import BaseModel

class AdminPasswordVerification(BaseModel):
    name: str
    password: str