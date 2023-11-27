# van a ir todas las rutas relacionadas con el usuario
from http.client import HTTPException
from models.tables import Multa
from fastapi import APIRouter, Depends, Request
from schemas.user import User, UserCreate, UserOut
from config.db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from controllers.user import create_user, exist_user, all_users, delete_users, exist_loan, get_associated_fine, exist_user_loan, email_validation, validate_password
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

@router.get("/management/fine/{correo}/{id_user}/{id_prestamo}")
def check_fines_and_deadlines(correo_usuario:str, id_usuario_prestamo: int, id_prestamo: int, db: Session = Depends(get_db)):
    exist_usr = exist_user(correo_usuario, db)#verificamos si el usuario existe
    exist_usr_loan = exist_user_loan(id_usuario_prestamo, db)#verificamos si el usuario tiene prestamos
    exist_loa = exist_loan(id_prestamo, db)#verificamos si el prestamo existe
    if not exist_usr:
        raise HTTPException(status_code=404, detail="User not exist")
    if not exist_usr_loan:
        raise HTTPException(status_code=404, detail="User has no loans")
    if not exist_loa:
        raise HTTPException(status_code=404, detail="Loan not exist")

    multa = get_associated_fine(id_usuario_prestamo, id_prestamo, db)

    if multa is None:
        raise HTTPException(status_code=404, detail="No fine associated with the user and loan")
    return {"fine": multa}


