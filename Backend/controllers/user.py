from fastapi.responses import JSONResponse
from schemas.physicalBook import PhysicalBook
from fastapi import HTTPException, status, Depends
from pydantic import EmailStr
from schemas.user import UserCreate, UserOut, User
from models.tables import Usuario
from sqlalchemy import func, text
from models.tables import LibroFisico, Multa, Prestamo, Usuario
from passlib.context import CryptContext
from controllers.hashing import Hasher
from typing import List, Optional

import jwt
from jwt import encode, decode
from functools import wraps

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(new_user: UserOut, db):
    hashed_password = password_context.hash(new_user.contrasena)
    #usr = new_user.dict(exclude={'contrasena'})
    #usr['contrasena']=hashed_password
    usr = Usuario(**new_user.dict(exclude={'contrasena'}), contrasena=hashed_password)
    # Crear el token
    secret_key = "tu_clave_secreta"
    algorithm = "HS256"
    payload = {
        "id": usr.id,
        "email": usr.correo,
        "role": usr.id_rol
    }
    token = jwt.encode(payload, secret_key, algorithm)
    usr.token = token
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr.token

def validar_token(token:str)->dict:
    dato:dict = decode(token, "tu_clave_secreta", algorithms=["HS256"])
    
    return dato

def exist_token(correo:str, contrasena:str,  db):
    usr = db.query(Usuario).filter(Usuario.correo == correo and Usuario.contrasena == contrasena).first()
    if not usr:
        return False
    return usr.token

def email_validation(correo: str, db):
    #comprueba que se ingrese un correo electrónico válido y que no sea nulo, lo hace EmailStr
    try:
        email = EmailStr._validate(correo)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Correo electrónico no válido"
        )

    return True

def validate_password(contrasena: str, db):
    if not any(char.isupper() for char in contrasena):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña debe contener al menos una letra mayúscula"
        )
    if not any(char.islower() for char in contrasena):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña debe contener al menos una letra minúscula"
        )
    if not any(char.isdigit() for char in contrasena):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña debe contener al menos un número"
        )
    return True

def exist_user(correo: str, db):
    usr = db.query(Usuario).filter(Usuario.correo == correo).first()
    return usr

def get_user(id: int, db):
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    return usr


def all_users(db):
    return db.query(Usuario).all()

def update_user(user_id: int, updated_user: UserOut, db) -> Optional[UserOut]:
        usr = get_user(user_id, db)
        if usr:
            usr.nombre = updated_user.nombre
            usr.correo = updated_user.correo
            usr.fechaNacimiento = updated_user.fechaNacimiento
            usr.id_rol = updated_user.id_rol
            usr.contrasena = usr.contrasena
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None
    
    
def delete_users(id: int, db):
    # Obtiene el valor del id antes de eliminar el registro
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    if not usr:
        print("El usuario no existe en la base de datos.")
        return None
    db.delete(usr)
    db.commit()
    max_id = db.query(func.max(Usuario.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE usuarios_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return usr


def exist_loan(id: int, db):#verificamos si el prestamo existe
    loan = db.query(Prestamo).filter(Prestamo.id == id).first()
    return loan

def get_associated_fine(id_user:int, id_prestamo: int, db):#obtenemos la multa asociada al prestamo
    multa = db.query(Multa).filter(Prestamo.id_usuario ==id_user , Multa.id_prestamo == id_prestamo).first()
    return multa

def exist_user_loan(id_user: int, db):#verificamos si el usuario tiene prestamos
    loan = db.query(Prestamo).filter(Prestamo.id_usuario == id_user).first()
    return loan

def get_user_by_email(email: str, db):
    return db.query(Usuario).filter(Usuario.correo == email).first()

        
        

