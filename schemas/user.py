from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    nombre: str
    correo: str
    fechaNacimiento: date

class UserCreate(User):
    contrasena: str
