from schemas.subcategory import SubCategory
from models.tables import *

def create_subcategory(new_subcategory: SubCategory, db):
    subcategory = SubCategoria(**new_subcategory.dict())
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory

def exist_subcategory(nombre: str, db):
    subcategory = db.query(SubCategoria).filter(SubCategoria.nombre == nombre).first()
    return subcategory

def all_subcategories(db):
    return db.query(SubCategoria).all()

def delete_subcategories(id: int, db):
    subcategory = db.query(SubCategoria).filter(SubCategoria.id == id).first()
    db.delete(subcategory)
    db.commit()
    return subcategory