from schemas.rol import RolCreate, RolOut
from models.tables import Rol
from sqlalchemy import func, text

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