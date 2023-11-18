from schemas.rol import RolCreate, RolOut
from models.tables import Rol

def create_rol(new_rol: RolCreate, db):
    rol = Rol(**new_rol.dict())
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol

def exist_rol(rol_nombre: str, db):
    rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
    return rol

def all_roles(db):
    return db.query(Rol).all()

def delete_rol(id: int, db):
    delRol = db.query(Rol).filter(Rol.id == id).first()
    db.delete(delRol)
    db.commit()
    return delRol