# van a ir todas las rutas relacionadas con el usuario
from http.client import HTTPException
from models.tables import Multa, Usuario
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from schemas.user import User, UserCreate, UserOut
from config.db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from controllers.user import create_user, exist_user, all_users, delete_users, exist_loan, get_associated_fine, exist_user_loan, email_validation, validate_password, password_context, exist_token, validar_token, update_user, decode_token
from controllers.email import send_welcome_email
from controllers.hashing import Hasher
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserOut


router = APIRouter()

@router.post("/register_user/")
async def register(new_user: UserCreate, db: Session = Depends(get_db)):
    # Validar el correo electrónico
    email_validation(new_user.correo, db)
    # Validar la contraseña
    validate_password(new_user.contrasena, db)
    # Verificar si el usuario ya existe
    if exist_user(new_user.correo, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya existe"
        )
        # Enviar correo electrónico al usuario
    await send_welcome_email(new_user.correo, new_user.nombre, Request)
    #result = create_user(new_user, db)
    
    #return result
    #return {'message' : 'Usuario registrado exitosamente'}
    token = create_user(new_user, db)
    return token


@router.post("/login_user")
def login(correo: str, contrasena: str, db: Session = Depends(get_db)):
    # Validar el correo electrónico
    email_validation(correo, db)
    # Verificar si el usuario existe
    usr = exist_user(correo, db)
    if not usr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no existe"
        )
    # Verificar si la contraseña es correcta
    if not password_context.verify(contrasena, usr.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La contraseña es incorrecta"
        )
    token = exist_token(correo, contrasena, db)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not exist"
        )
    
    # return usr, token
    return token

#Para la validacion del token
class Portador(HTTPBearer):
    async def __call__(self, request: Request):
        try:
            token = await super().__call__(request)
            datos = validar_token(token.credentials)
            correo = datos.get("email")

            if correo is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="El token no contiene la información del correo"
                )

            # Verifica aquí si el usuario tiene los permisos necesarios para acceder a la ruta
            # Puedes implementar una función has_permission(token, ruta) para esto

            return token

        except HTTPException as e:
            raise e  # Propaga excepciones HTTP ya lanzadas
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Error al procesar el token"
            ) from e
          

# obtener usuario por correo
@router.get("get_user/{correo}", dependencies=[Depends(Portador())])
def get_user(correo: str, db: Session = Depends(get_db)):
    exist = exist_user(correo, db)
    if not exist:
        return {"message": "User not exist"}

    return UserOut(**exist.__dict__)


# obtener todos los usuarios
@router.get("/all_users/")
def get_all_users(db: Session = Depends(get_db)):
    return all_users(db)

#Ruta para actualizar un usuario
@router.put("/update_user/{user_id}", dependencies=[Depends(Portador())])
def update_users(user_id:int, update_usr:User, db: Session = Depends(get_db)):
    usr = update_user(user_id, update_usr, db)
    if usr:
        return usr
    raise HTTPException(status_code=404, detail="User not found")
    

# eliminar usuarios por id
@router.delete("/delete/{user_id}", dependencies=[Depends(Portador())])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    userDeleted = delete_users(user_id, db)
    if not userDeleted:
        return {"message": "User not exist"}
    return {
        "message": "User deleted successfully",
        "user": User(**userDeleted.__dict__),
    }


@router.get("/management_fine/{correo}/{id_user}/{id_prestamo}", dependencies=[Depends(Portador())])
def check_fines_and_deadlines(correo_usuario: str, id_usuario_prestamo: int, id_prestamo: int, db: Session = Depends(get_db)):
    # verificamos si el usuario existe
    exist_usr = exist_user(correo_usuario, db)
    # verificamos si el usuario tiene prestamos
    exist_usr_loan = exist_user_loan(id_usuario_prestamo, db)
    # verificamos si el prestamo existe
    exist_loa = exist_loan(id_prestamo, db)
    if not exist_usr:
        raise HTTPException(status_code=404, detail="User not exist")
    if not exist_usr_loan:
        raise HTTPException(status_code=404, detail="User has no loans")
    if not exist_loa:
        raise HTTPException(status_code=404, detail="Loan not exist")

    multa = get_associated_fine(id_usuario_prestamo, id_prestamo, db)

    if multa is None:
        raise HTTPException(
            status_code=404, detail="No fine associated with the user and loan")
    return {"fine": multa}

@router.get("/id_userToken/{token}", dependencies=[Depends(Portador())])
def id_user_token(token: str, db: Session = Depends(get_db)):
    respone = decode_token(token,db)
    return respone




