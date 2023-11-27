from schemas.physicalBook import PhysicalBook
from fastapi import HTTPException, status
from pydantic import EmailStr
from schemas.user import UserCreate
from models.tables import Usuario
from sqlalchemy import func, text
from models.tables import LibroFisico, Multa, Prestamo, Usuario

def create_user(new_user: UserCreate, db):
    usr = Usuario(**new_user.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr

def email_validation(correo: str, db):
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
    usr = db.query(Usuario).filter(Usuario.correo == correo).first()
    return usr

def get_user(id: int, db):
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    return usr


def all_users(db):
    return db.query(Usuario).all()

def delete_users(id: int, db):
    # Obtiene el valor del id antes de eliminar el registro
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    db.delete(usr)
    db.commit()
    max_id = db.query(func.max(Usuario.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE usuarios_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return usr

def exist_loan(id: int, db):#verificamos si el prestamo existe
    loan = db.query(Prestamo).filter(Prestamo.id == id).first()
    return loan

def get_associated_fine(id_user:int, id_prestamo: int, db):#obtenemos la multa asociada al prestamo
    multa = db.query(Multa).filter(Prestamo.id_usuario ==id_user , Multa.id_prestamo == id_prestamo).first()
    return multa

def exist_user_loan(id_user: int, db):#verificamos si el usuario tiene prestamos
    loan = db.query(Prestamo).filter(Prestamo.id_usuario == id_user).first()
    return loan


    
            
        

