from schemas.rol import RolCreate, RolOut
from models.tables import Rol
from sqlalchemy import func, text
from typing import List, Optional

def create_rol(new_rol: RolCreate, db):
    """
    Crea un nuevo rol en la base de datos.
    Args:
        new_rol (RolCreate): Objeto que contiene la información del nuevo rol.
        db: Sesión de la base de datos.
    Returns:
        Rol: Objeto del rol creado.
    """
    rol = Rol(**new_rol.dict())
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol

def exist_rol(rol_nombre: str, db):
    """
    Verifica la existencia de un rol en la base de datos por su nombre.
    Args:
        rol_nombre (str): Nombre del rol.
        db: Sesión de la base de datos.
    Returns:
        Rol or None: Objeto del rol si existe, None si no se encuentra.
    """
    rol = db.query(Rol).filter(func.upper(Rol.nombre) == rol_nombre.upper()).first()
    return rol

def exist_rolId(id_rol:int, db):
    """
    Verifica la existencia de un rol en la base de datos por su ID.
    Args:
        id_rol (int): ID del rol.
        db: Sesión de la base de datos.
    Returns:
        Rol or None: Objeto del rol si existe, None si no se encuentra.
    """
    rol = db.query(Rol).filter(Rol.id == id_rol).first()
    return rol

def get_rol_id(name_rol:str, db):
    """
    Obtiene el ID de un rol en la base de datos por su nombre.
    Args:
        name_rol (str): Nombre del rol.
        db: Sesión de la base de datos.
    Returns:
        int or None: ID del rol si existe, None si no se encuentra.
    """
    rol = db.query(Rol).filter(func.upper(Rol.nombre) == name_rol.upper()).first()
    return rol.id

def all_roles(db):
    """
    Obtiene todos los roles de la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        list: Lista de objetos de roles.
    """
    return db.query(Rol).all()

def delete_rol(id: int, db):
    """
    Elimina un rol de la base de datos por su ID.
    Args:
        id (int): ID del rol.
        db: Sesión de la base de datos.
    Returns:
        Rol or None: Objeto del rol eliminado si existe, None si no se encuentra.
    """
    delRol = db.query(Rol).filter(Rol.id == id).first()
    db.delete(delRol)
    db.commit()
    max_id = db.query(func.max(Rol.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE roles_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return delRol

def get_rolcreate(id: int, db):
    cat = db.query(Rol).filter(Rol.id == id).first()
    return cat

def update_rolcreate(rolcreate_id: int, updated_rolcreate: RolCreate, db) -> Optional[RolCreate]:
        usr = get_rolcreate(rolcreate_id, db)
        if usr:
            usr.nombre = updated_rolcreate.nombre
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None