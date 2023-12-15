from schemas.category import Category
from models.tables import *
from sqlalchemy import func, text
from typing import List, Optional


def create_category(new_category: Category, db):
    cat = Categoria(**new_category.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def exist_category(nombre: str, db):
    cat = db.query(Categoria).filter(func.upper(Categoria.nombre) == nombre.upper()).first()
    return cat


def all_categories(db):
    return db.query(Categoria).all()

def delete_categories(id: int, db):
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    db.delete(cat)
    db.commit()
    db.commit()
    max_id = db.query(func.max(Categoria.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE categorias_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return cat

def get_category(id: int, db):
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    return cat


def update_category(category_id: int, updated_category: Category, db) -> Optional[Category]:
        usr = get_category(category_id, db)
        if usr:
            usr.nombre = updated_category.nombre
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None