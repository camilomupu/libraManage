from schemas.subcategory import SubCategory
from models.tables import *
from sqlalchemy import func, text

def create_subcategory(new_subcategory: SubCategory, db):
    subcategory = SubCategoria(**new_subcategory.dict())
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory

def exist_subcategory(nombre: str, db):
    subcategory = db.query(SubCategoria).filter(func.upper(SubCategoria.nombre) == nombre.upper()).first()
    return subcategory

def get_subcategory(id: int, db):
    subcategory = db.query(SubCategoria).filter(SubCategoria.id == id).first()
    return subcategory

def all_subcategories(db):
    return db.query(SubCategoria).all()

def delete_subcategories(id: int, db):
    subcategory = db.query(SubCategoria).filter(SubCategoria.id == id).first()
    db.delete(subcategory)
    db.commit()
    max_id = db.query(func.max(SubCategoria.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE subcategorias_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return subcategory