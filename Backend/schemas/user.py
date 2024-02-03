from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    nombre: str
    correo: str
    fechaNacimiento: date


class UserCreate(User):
    contrasena: str
    

class UserUpdate(User):
    id_rol: int
    
class UserEdit(User):
    id_rol : int
    token : str
    
    
    

class UserOut(User):
    id: int
    token : str
    id_rol: int
    
    
