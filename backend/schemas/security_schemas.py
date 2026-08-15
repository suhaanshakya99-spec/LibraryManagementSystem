from pydantic import BaseModel

class Payload_Data(BaseModel):
    id:int
    email:str
    