from schemas.category import Category
from models.tables import *

def create_category(new_category: Category, db):
    cat = Categoria(**new_category.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def exist_category(nombre: str, db):
    cat = db.query(Categoria).filter(Categoria.nombre == nombre).first()
    return cat

def all_categories(db):
    return db.query(Categoria).all()

def delete_categories(id: str, db):
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    db.delete(cat)
    db.commit()
    return cat