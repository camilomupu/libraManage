from schemas.subcategory import SubCategory
from models.tables import *
from sqlalchemy import func, text
from typing import List, Optional

def create_subcategory(new_subcategory: SubCategory, db):
    """
    Crea una nueva subcategoría en la base de datos.
    Args:
        new_subcategory (SubCategory): Objeto que contiene la información de la nueva subcategoría.
        db: Sesión de la base de datos.
    Returns:
        SubCategory: Objeto de la subcategoría creada.
    """
    subcategory = SubCategoria(**new_subcategory.dict())
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory

def exist_subcategory(nombre: str, db):
    """
    Verifica la existencia de una subcategoría en la base de datos por su nombre.
    Args:
        nombre (str): Nombre de la subcategoría.
        db: Sesión de la base de datos.
    Returns:
        SubCategory or None: Objeto de la subcategoría si existe, None si no se encuentra.
    """
    subcategory = db.query(SubCategoria).filter(func.upper(SubCategoria.nombre) == nombre.upper()).first()
    return subcategory

def get_subcategory(id: int, db):
    """
    Obtiene una subcategoría de la base de datos por su ID.
    Args:
        id (int): ID de la subcategoría.
        db: Sesión de la base de datos.
    Returns:
        SubCategory or None: Objeto de la subcategoría si existe, None si no se encuentra.
    """
    subcategory = db.query(SubCategoria).filter(SubCategoria.id == id).first()
    return subcategory

def all_subcategories(db):
    """
    Obtiene todas las subcategorías de la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        list: Lista de objetos de subcategorías.
    """
    return db.query(SubCategoria).all()

def delete_subcategories(id: int, db):
    """
    Elimina una subcategoría de la base de datos por su ID.
    Args:
        id (int): ID de la subcategoría.
        db: Sesión de la base de datos.
    Returns:
        SubCategory or None: Objeto de la subcategoría eliminada si existe, None si no se encuentra.
    """
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