from datetime import date
from pydantic import BaseModel

class RolCreate(BaseModel):
    nombre: str

class RolOut(RolCreate):
    id: int 