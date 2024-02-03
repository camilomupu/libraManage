from fastapi.responses import JSONResponse
from schemas.physicalBook import PhysicalBook
from fastapi import HTTPException, status, Depends
from pydantic import EmailStr
from schemas.user import UserCreate, UserOut, UserEdit
from models.tables import Usuario
from sqlalchemy import func, text
from models.tables import LibroFisico, Multa, Prestamo, Usuario
from controllers.rol import get_rol_id
from passlib.context import CryptContext
from controllers.hashing import Hasher
from typing import List, Optional

import jwt
from jwt import encode, decode
from functools import wraps

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(new_user: UserOut, db):
    """
    Crea un nuevo usuario en la base de datos, generando y asignando un token JWT.
    Args:
        new_user (UserOut): Objeto que contiene la información del nuevo usuario.
        db: Sesión de la base de datos.
    Returns:
        str: Token JWT generado para el nuevo usuario.
    """
    hashed_password = password_context.hash(new_user.contrasena)
    
    #usr = new_user.dict(exclude={'contrasena'})
    #usr['contrasena']=hashed_password
    usr = Usuario(**new_user.dict(exclude={'contrasena'}), contrasena=hashed_password)
    # Crear el token
    secret_key = "tu_clave_secreta"
    algorithm = "HS256"
    rol_id = get_rol_id("Cliente", db)
    usr.id_rol = rol_id
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
    """
    Valida y decodifica un token JWT.
    Args:
        token (str): Token JWT a validar y decodificar.
    Returns:
        dict: Datos contenidos en el token decodificado.
    """
    dato:dict = decode(token, "tu_clave_secreta", algorithms=["HS256"])
    
    return dato

def exist_token(correo:str, contrasena:str,  db):
    """
    Verifica la existencia de un token asociado a un usuario.
    Args:
        correo (str): Correo electrónico del usuario.
        contrasena (str): Contraseña del usuario.
        db: Sesión de la base de datos.
    Returns:
        str or None: Token del usuario si existe, None si no se encuentra.
    """
    usr = db.query(Usuario).filter(Usuario.correo == correo and Usuario.contrasena == contrasena).first()
    if not usr:
        return False
    return usr.token

def email_validation(correo: str, db):
    """
    Valida si el formato del correo electrónico proporcionado es válido.
    Args:
        correo (str): Correo electrónico a validar.
        db: Sesión de la base de datos.
    Raises:
        HTTPException: Excepción HTTP 422 si el correo electrónico no es válido.
    """
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
    """
    Valida la fortaleza de la contraseña proporcionada.
    Args:
        contrasena (str): Contraseña a validar.
        db: Sesión de la base de datos.
    Raises:
        HTTPException: Excepción HTTP 422 con detalles específicos si la contraseña no cumple con los requisitos.
    """
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
    """
    Verifica la existencia de un usuario en la base de datos por su correo electrónico.
    Args:
        correo (str): Correo electrónico del usuario.
        db: Sesión de la base de datos.
    Returns:
        Usuario or None: Objeto del usuario si existe, None si no se encuentra.
    """
    usr = db.query(Usuario).filter(Usuario.correo == correo).first()
    return usr

def get_user(id: int, db):
    """
    Obtiene un usuario de la base de datos por su ID.
    Args:
        id (int): ID del usuario.
        db: Sesión de la base de datos.
    Returns:
        Usuario or None: Objeto del usuario si existe, None si no se encuentra.
    """
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    return usr

def get_token (id: int, db):
    """
    Obtiene el token de un usuario de la base de datos por su ID.
    Args:
        id (int): ID del usuario.
        db: Sesión de la base de datos.
    Returns:
        str or None: Token del usuario si existe, None si no se encuentra.
    """
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    return usr.token


def all_users(db):
    """
    Obtiene todos los usuarios de la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        list: Lista de objetos de usuarios.
    """
    return db.query(Usuario).all()

def update_user(user_id: int, updated_user: UserEdit, db) -> Optional[UserOut]:
        """
        Actualiza la información de un usuario en la base de datos.
        Args:
            user_id (int): ID del usuario a actualizar.
            updated_user (UserEdit): Objeto que contiene la información actualizada del usuario.
            db: Sesión de la base de datos.
        Returns:
            Usuario or None: Objeto del usuario actualizado si existe, None si no se encuentra.
        """
        usr = get_user(user_id, db)
        secret_key = "tu_clave_secreta"
        algorithm = "HS256"
        
        if usr:
            payload = {
            "id": usr.id,
            "email": usr.correo,
            "role": updated_user.id_rol
            }
            usr.nombre = updated_user.nombre
            usr.correo = updated_user.correo
            usr.fechaNacimiento = updated_user.fechaNacimiento
            usr.id_rol = updated_user.id_rol
            usr.token = jwt.encode(payload, secret_key, algorithm)
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None

def exist_email(email: str, db):
    """
    Verifica la existencia de un usuario en la base de datos por su correo electrónico.
    Args:
        email (str): Correo electrónico del usuario.
        db: Sesión de la base de datos.
    Returns:
        Usuario or None: Objeto del usuario si existe, None si no se encuentra.
    """
    usr = db.query(Usuario).filter(Usuario.correo == email).first()
    return usr
    
    
def delete_users(id: int, db):
    """
    Elimina un usuario de la base de datos por su ID.
    Args:
        id (int): ID del usuario a eliminar.
        db: Sesión de la base de datos.
    Returns:
        Usuario or None: Objeto del usuario eliminado si existe, None si no se encuentra.
    """
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
    """
    Verifica la existencia de un préstamo en la base de datos por su ID.
    Args:
        id (int): ID del préstamo.
        db: Sesión de la base de datos.
    Returns:
        Prestamo or None: Objeto del préstamo si existe, None si no se encuentra.
    """
    loan = db.query(Prestamo).filter(Prestamo.id == id).first()
    return loan

def get_associated_fine(id_user:int, id_prestamo: int, db):#obtenemos la multa asociada al prestamo
    """
    Obtiene la multa asociada a un préstamo en la base de datos.
    Args:
        id_user (int): ID del usuario.
        id_prestamo (int): ID del préstamo.
        db: Sesión de la base de datos.
    Returns:
        Multa or None: Objeto de la multa si existe, None si no se encuentra.
    """
    multa = db.query(Multa).filter(Prestamo.id_usuario ==id_user , Multa.id_prestamo == id_prestamo).first()
    return multa

def exist_user_loan(id_user: int, db):#verificamos si el usuario tiene prestamos
    """
    Verifica si un usuario tiene préstamos en la base de datos.
    Args:
        id_user (int): ID del usuario.
        db: Sesión de la base de datos.
    Returns:
        Prestamo or None: Objeto del préstamo si existe, None si no se encuentra.
    """
    loan = db.query(Prestamo).filter(Prestamo.id_usuario == id_user).first()
    return loan

def get_user_by_email(email: str, db):
    """
    Obtiene un usuario de la base de datos por su correo electrónico.
    Args:
        email (str): Correo electrónico del usuario.
        db: Sesión de la base de datos.
    Returns:
        Usuario or None: Objeto del usuario si existe, None si no se encuentra.
    """
    return db.query(Usuario).filter(Usuario.correo == email).first()

def return_id_user(email: str, db):
    """
    Obtiene el ID de un usuario de la base de datos por su correo electrónico.
    Args:
        email (str): Correo electrónico del usuario.
        db: Sesión de la base de datos.
    Returns:
        int or None: ID del usuario si existe, None si no se encuentra.
    """
    return db.query(Usuario.id).filter(Usuario.correo == email).first()

def decode_token(token: str, db):
    """
    Decodifica un token JWT y obtiene el ID del usuario asociado.
    Args:
        token (str): Token JWT a decodificar.
        db: Sesión de la base de datos.
    Returns:
        int or False: ID del usuario si la decodificación es exitosa, False si hay algún error.
    """
    try:
        decoded_token = jwt.decode(token, "tu_clave_secreta", algorithms=["HS256"])
        correo = decoded_token.get("email")
        print(correo)
        usuario = return_id_user(correo, db)
        print(usuario)
        if usuario:
            return usuario.id
        else:
            return False
    except:
        return False

        
        

