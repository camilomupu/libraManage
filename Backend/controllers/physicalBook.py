from schemas.physicalBook import PhysicalBook
from models.tables import *
from sqlalchemy import func, text

def create_physicalBook(new_book: PhysicalBook, db):
    book = LibroFisico(**new_book.__dict__)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def exist_physicalBook(titulo: str, id_author: int, db):
    book = db.query(LibroFisico).filter((func.upper(LibroFisico.titulo) == titulo.upper()) & (LibroFisico.id_autor == id_author)).first()
    return book

def get_physicalBook(id: int, db):
    book = db.query(LibroFisico).filter(LibroFisico.id == id).first()
    return book

def all_physicalBook(db):
    return db.query(LibroFisico).all()

def delete_physicalBook(id: int, db):
    book = db.query(LibroFisico).filter(LibroFisico.id == id).first()
    db.delete(book)
    db.commit()
    max_id = db.query(func.max(LibroFisico.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE librosFisicos_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return book
    