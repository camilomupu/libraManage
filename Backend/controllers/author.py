from schemas.author import Author
from models.tables import *
from sqlalchemy import func, text

def create_author(new_author: Author, db):
    """
    Crea un nuevo registro de autor en la base de datos.
    Args:
        new_author (Author): Objeto que contiene la información del nuevo autor.
        db: Sesión de la base de datos.
    Returns:
        Author: El objeto Author recién creado.
    """
    author = Autor(**new_author.dict())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def exist_author(nombre: str, db):
    """
    Verifica si existe un autor con el nombre especificado en la base de datos.
    Args:
        nombre (str): Nombre del autor a buscar (case-insensitive).
        db: Sesión de la base de datos.
    Returns:
        Author or None: El objeto Author si existe, None si no se encuentra.
    """
    author = db.query(Autor).filter(func.upper(Autor.nombre) == nombre.upper()).first()
    return author

def get_author(id: int, db):
    """
    Obtiene un autor por su ID.
    Args:
        id (int): ID del autor a recuperar.
        db: Sesión de la base de datos.
    Returns:
        Author or None: El objeto Author si se encuentra, None si no se encuentra.
    """
    author = db.query(Autor).filter(Autor.id == id).first()
    return author

def all_authors(db):
    """
    Obtiene todos los registros de autores en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        List[Author]: Lista que contiene todos los registros de Author.
    """
    return db.query(Autor).all()

def delete_authors(id: int, db):
    """
    Elimina un autor por su ID, reiniciando la secuencia de ID después de la eliminación.
    Args:
        id (int): ID del autor a eliminar.
        db: Sesión de la base de datos.
    Returns:
        Author or None: El objeto Author eliminado si se encuentra, None si no se encuentra.
    """
    author = db.query(Autor).filter(Autor.id == id).first()
    db.delete(author)
    db.commit()
    max_id = db.query(func.max(Autor.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE autores_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    
    return author