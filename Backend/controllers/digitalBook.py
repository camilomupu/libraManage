from schemas.digitalBook import DigitalBookCreate
from models.tables import *
from sqlalchemy import func, text

def create_dBook(nuevo_dBook: DigitalBookCreate, db):
    libro = LibroDigital(**nuevo_dBook.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro

def exist_dBook(title: str, id_autor: int, db):
    libro = db.query(LibroDigital).filter((func.upper(LibroDigital.titulo) == title.upper()) & (LibroDigital.id_autor == id_autor)).first()
    return libro

def get_dBook(id: int, db):
    libro = db.query(LibroDigital).filter(LibroDigital.id == id).first()
    return libro

def all_dBooks(db):
    return db.query(LibroDigital).all()

def delete_dBook(id: int, db):
    libro = db.query(LibroDigital).filter(LibroDigital.id == id).first()
    db.delete(libro)
    db.commit()
    max_id = db.query(func.max(LibroDigital.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE librosDigitales_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return libro

def exist_user_admin(correo:str, db): #Verificamos si el usuario es administrador
    user = db.query(Usuario).filter(Usuario.correo == correo).first()
    if user is None: #Verificamos si el usuario existe
        return False
    if user.id_rol is None: #Verificamos si el usuario tiene rol
        return False
    rol = db.query(Rol).filter(Rol.id == user.id_rol).first()

    if rol is None: #Verificamos si el rol existe
        return False
    if rol.nombre == "Administrador" or rol.nombre == "administrador": #Verificamos si el rol es administrador
        return True
    return False