# van a ir todas las rutas relacionadas con el usuario
from fastapi import APIRouter, Depends, Request
from schemas.user import User, UserCreate, UserOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.user import create_user, exist_user, all_users, delete_users, email_validation, validate_password
from controllers.email import send_welcome_email


router = APIRouter()


# nuevo usuario
@router.post("/")
async def create_new_user(usuario: UserCreate, db: Session = Depends(get_db)):
    exist = exist_user(usuario.correo, db)
    if exist:
        return {"message": "User already exist"}
    
    #Comprobamos el correo
    email_validation(usuario.correo, db)
    #Comprobamos la contraseña
    validate_password(usuario.contrasena, db)
    new_user = create_user(usuario, db)
    
    # Enviar correo electrónico al usuario
    await send_welcome_email(new_user.correo, new_user.nombre, Request)
    
    return User(**new_user.__dict__)


# obtener usuario por correo
@router.get("/{correo}")
def get_user(correo: str, db: Session = Depends(get_db)):
    exist = exist_user(correo, db)
    if not exist:
        return {"message": "User not exist"}

    return UserOut(**exist.__dict__)


# obtener todos los usuarios
@router.get("/all_users/")
def get_all_users(db: Session = Depends(get_db)):
    return all_users(db)


# eliminar usuarios por id
@router.delete("/delete/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    userDeleted = delete_users(id, db)
    if not userDeleted:
        return {"message": "User not exist"}
    return {
        "message": "User deleted successfully",
        "user": User(**userDeleted.__dict__),
    }
