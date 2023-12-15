from schemas.subcategory import SubCategory
from models.tables import *
from sqlalchemy import func, text
from typing import List, Optional

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
    print(id)
    subcategory = db.query(SubCategoria).filter(SubCategoria.id == id).first()
    
    db.delete(subcategory)
    db.commit()
    return subcategory

def update_SubCategory(SubCategory_id: int, updated_SubCategory: SubCategory, db) -> Optional[SubCategory]:
        usr = get_subcategory(SubCategory_id, db)
        if usr:
            usr.nombre = updated_SubCategory.nombre
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None