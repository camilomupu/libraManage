from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    nombre: str
    correo: str
    fechaNacimiento: date
    id_rol: int

class UserCreate(User):
    contrasena: str
