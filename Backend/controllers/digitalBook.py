from schemas.digitalBook import DigitalBookCreate
from models.tables import *

def create_dBook(nuevo_dBook: DigitalBookCreate, db):

    libro = LibroDigital(**nuevo_dBook.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro

def exist_dBook(title: str, id_autor: int, db):
    libro = db.query(LibroDigital).filter(LibroDigital.titulo == title and LibroDigital.id_autor == id_autor).first()
    return libro

def all_dBooks(db):
    return db.query(LibroDigital).all()

def delete_dBook(id: int, db):
    libro = db.query(LibroDigital).filter(LibroDigital.id == id).first()
    db.delete(libro)
    db.commit()
    return libro