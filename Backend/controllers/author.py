from schemas.author import Author
from models.tables import *
from sqlalchemy import func

def create_author(new_author: Author, db):
    author = Autor(**new_author.dict())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def exist_author(nombre: str, db):
    author = db.query(Autor).filter(func.upper(Autor.nombre) == nombre.upper()).first()
    return author

def get_author(id: int, db):
    author = db.query(Autor).filter(Autor.id == id).first()
    return author

def all_authors(db):
    return db.query(Autor).all()

def delete_authors(id: int, db):
    author = db.query(Autor).filter(Autor.id == id).first()
    db.delete(author)
    db.commit()
    return author