from schemas.category import Category
from models.tables import *
from sqlalchemy import func

def create_category(new_category: Category, db):
    cat = Categoria(**new_category.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def exist_category(nombre: str, db):
    cat = db.query(Categoria).filter(func.upper(Categoria.nombre) == nombre.upper()).first()
    return cat

def get_category(id: int, db):
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    return cat

def all_categories(db):
    return db.query(Categoria).all()

def delete_categories(id: int, db):
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    db.delete(cat)
    db.commit()
    return cat