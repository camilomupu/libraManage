#van a ir todas las rutas relacionadas con el rol
from fastapi import APIRouter, Depends
from schemas.rol import RolCreate, RolOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.rol import create_rol, exist_rol, all_roles, delete_rol

router = APIRouter()

#crear rol
@router.post("/rolcreate/")
def create_new_rol(new_rol: RolCreate, db: Session = Depends(get_db)):
    exist = exist_rol(new_rol.nombre, db)
    if exist:
        return {"message": "Rol already exist"}

    rol = create_rol(new_rol, db)
    return rol

#obtener todos los roles
@router.get("/rol/",response_model=list[RolCreate])
def get_all_roles(db: Session = Depends(get_db)):
    return all_roles(db)

#obtener rol por nombre
@router.get("/rol/{nombre}")
def get_rol(nombre: str, db: Session = Depends(get_db)):
    exist = exist_rol(nombre, db)
    if not exist:
        return {"message": "Rol not exist"}
    
    return RolOut(**exist.__dict__)

#eliminar roles por id
@router.delete("/rol/delete/{id}")
def delete_roles(id: str, db: Session = Depends(get_db)):
    rolDeleted = delete_rol(id, db)
    if not rolDeleted:
        return {"message": "User not exist"}
    return {"message": "User deleted successfully", "user": RolOut(**rolDeleted.__dict__)}