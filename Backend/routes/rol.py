#van a ir todas las rutas relacionadas con el rol
from fastapi import APIRouter, Depends
from schemas.rol import RolCreate, RolOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.rol import create_rol, exist_rol, all_roles, delete_rol, exist_rolId
from routes.user import Portador

router = APIRouter()

#crear rol
@router.post("/rolcreate/")
def create_new_rol(new_rol: RolCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo rol.
    Args:
        new_rol (RolCreate): Datos del nuevo rol.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        Rol: Rol creado.
    """
    exist = exist_rol(new_rol.nombre, db)
    if exist:
        return {"message": "Rol already exist"}

    rol = create_rol(new_rol, db)
    return rol

#obtener todos los roles
@router.get("/all_roles/",response_model=list[RolOut])
def get_all_roles(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los roles.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        List[RolOut]: Lista de roles.
    """
    return all_roles(db)

#obtener rol por nombre
@router.get("/rol/{nombre}", dependencies=[Depends(Portador())])
def get_rol(nombre: str, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un rol por su nombre.
    Args:
        nombre (str): Nombre del rol.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        RolOut: Detalles del rol.
    """
    exist = exist_rol(nombre, db)
    if not exist:
        return {"message": "Rol not exist"}
    
    return RolOut(**exist.__dict__)

@router.get("/get_rol/{id}", dependencies=[Depends(Portador())])
def get_rolId(id_rol:int, db:Session=Depends(get_db)):
    """
    Endpoint para obtener un rol por su ID.
    Args:
        id_rol (int): ID del rol.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        RolOut: Detalles del rol.
    """
    exist = exist_rolId(id_rol, db)
    if not exist:
        return {"message": "Rol not exist"}
    return RolOut(**exist.__dict__)

#eliminar roles por id
@router.delete("/rol/delete/{id}")
def delete_roles(id: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar un rol por su ID.
    Args:
        id (int): ID del rol.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Mensaje indicando que el rol se eliminó correctamente o que no existe.
    """
    rolDeleted = delete_rol(id, db)
    if not rolDeleted:
        return {"message": "User not exist"}
    return {"message": "User deleted successfully", "user": RolOut(**rolDeleted.__dict__)}