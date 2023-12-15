from schemas.category import Category
from models.tables import *
from sqlalchemy import func, text

def create_category(new_category: Category, db):
    """
    Crea un nuevo registro de categoría en la base de datos.
    Args:
        new_category (Category): Objeto que contiene la información de la nueva categoría.
        db: Sesión de la base de datos.
    Returns:
        Category: El objeto Category recién creado.
    """
    cat = Categoria(**new_category.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def exist_category(nombre: str, db):
    """
    Verifica si existe una categoría con el nombre especificado en la base de datos.
    Args:
        nombre (str): Nombre de la categoría a buscar (case-insensitive).
        db: Sesión de la base de datos.
    Returns:
        Category or None: El objeto Category si existe, None si no se encuentra.
    """
    cat = db.query(Categoria).filter(func.upper(Categoria.nombre) == nombre.upper()).first()
    return cat

def get_category(id: int, db):
    """
    Obtiene una categoría por su ID.
    Args:
        id (int): ID de la categoría a recuperar.
        db: Sesión de la base de datos.
    Returns:
        Category or None: El objeto Category si se encuentra, None si no se encuentra.
    """
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    return cat

def all_categories(db):
    """
    Obtiene todos los registros de categorías en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        List[Category]: Lista que contiene todos los registros de Category.
    """
    return db.query(Categoria).all()

def delete_categories(id: int, db):
    """
    Elimina una categoría por su ID, reiniciando la secuencia de ID después de la eliminación.
    Args:
        id (int): ID de la categoría a eliminar.
        db: Sesión de la base de datos.
    Returns:
        Category or None: El objeto Category eliminado si se encuentra, None si no se encuentra.
    """
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    db.delete(cat)
    db.commit()
    db.commit()
    max_id = db.query(func.max(Categoria.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE categorias_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return cat