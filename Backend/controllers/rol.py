from schemas.rol import RolCreate, RolOut
from models.tables import Rol
from sqlalchemy import func, text
from typing import List, Optional

def create_rol(new_rol: RolCreate, db):
    rol = Rol(**new_rol.dict())
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol

def exist_rol(rol_nombre: str, db):
    rol = db.query(Rol).filter(func.upper(Rol.nombre) == rol_nombre.upper()).first()
    return rol

def all_roles(db):
    return db.query(Rol).all()

def delete_rol(id: int, db):
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