from schemas.author import Author
from models.tables import *
from sqlalchemy import func, text
from typing import List, Optional

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
    max_id = db.query(func.max(Autor.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE autores_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    
    return author

def get_author(id: int, db):
    cat = db.query(Autor).filter(Autor.id == id).first()
    return cat


def update_author(author_id: int, updated_author: Author, db) -> Optional[Author]:
        usr = get_author(author_id, db)
        if usr:
            usr.nombre = updated_author.nombre
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None