from schemas.physicalBook import PhysicalBook
from models.tables import *

def create_physicalBook(new_book: PhysicalBook, db):
    book = LibroFisico(**new_book.__dict__)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def exist_physicalBook(titulo: str, db):
    book = db.query(LibroFisico).filter(LibroFisico.titulo == titulo).first()
    return book

def all_physicalBook(db):
    return db.query(LibroFisico).all()

def delete_physicalBook(id: str, db):
    book = db.query(LibroFisico).filter(LibroFisico.id == id).first()
    db.delete(book)
    db.commit()
    return book
    