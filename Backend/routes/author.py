from fastapi import APIRouter, Depends
from schemas.author import Author, AuthorOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.author import create_author, exist_author, all_authors, delete_authors
from routes.user import Portador


router = APIRouter()

#nueva author
@router.post("/new_author/")
def create_new_author(author: Author, db: Session = Depends(get_db)):
    """
    Crea un nuevo autor en la base de datos.
    Args:
        author (Author): Datos del nuevo autor.
        db (Session): Sesión de la base de datos.
    Returns:
        AuthorOut or dict: Si el autor se crea con éxito, devuelve los datos del autor creado.
                           Si el autor ya existe, devuelve un mensaje indicando que el autor ya existe.
    """
    exist = exist_author(author.nombre, db)
    if exist:
        return {"message": "author already exist"}
    new_author = create_author(author,db)
    return Author(**new_author.__dict__)

#obtener author por nombre
@router.get("/author/{nombre}", dependencies=[Depends(Portador())])
def get_author(nombre: str, db: Session = Depends(get_db)):
    """
    Obtiene los datos de un autor por su nombre.

    Args:
        nombre (str): Nombre del autor.
        db (Session): Sesión de la base de datos.

    Returns:
        AuthorOut or dict: Si el autor existe, devuelve los datos del autor.
                           Si el autor no existe, devuelve un mensaje indicando que el autor no existe.
    """
    exist = exist_author(nombre, db)
    if not exist:
        return {"message": "author not exist"}
    
    return AuthorOut(**exist.__dict__)

#obtener todas las authors
@router.get("/all_authors/", response_model=list[AuthorOut])
def get_all_authors(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los autores.
    Args:
        db (Session): Sesión de la base de datos.
    Returns:
        list[AuthorOut]: Lista de autores.
    """
    return all_authors(db)

#eliminar authors por id  
@router.delete("/delete_authors/{id}")
def delete_authorss(id: int, db: Session = Depends(get_db)):
    """
    Elimina un autor por su ID.
    Args:
        id (int): ID del autor a eliminar.
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Si el autor se elimina con éxito, devuelve un mensaje indicando que el autor se eliminó correctamente.
              Si el autor no existe, devuelve un mensaje indicando que el autor no existe.
    """
    authorDeleted = delete_authors(id, db)
    if not authorDeleted:
        return {"message": "author not exist"}
    return {"message": "author deleted successfully"}