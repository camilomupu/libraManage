
from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from schemas.physicalBook import PhysicalBook, PhysicalBookOut
from config.db import get_db, upload_img
from sqlalchemy.orm import Session
from controllers.physicalBook import create_physicalBook, exist_physicalBook, all_physicalBook, delete_physicalBook, exist_user_admin, search_physical_book,register_physicalBook, update_physicalbook
from controllers.author import get_author
from controllers.category import get_category
from controllers.subcategory import get_subcategory
from routes.user import Portador


router = APIRouter()

    
@router.post("/register_physicalBooks/")
async def register_physicalBooks(titulo:str,descripcion:str,ubicacion:str,
                  estado:str, id_autor:int, id_categoria:int, id_subcategoria:int
                  , file: UploadFile = None, url_image:str = None, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo libro físico.
    Args:
        correo (str): Correo del usuario administrador.
        titulo (str): Título del libro físico.
        descripcion (str): Descripción del libro físico.
        ubicacion (str): Ubicación física del libro.
        estado (str): Estado actual del libro físico.
        id_autor (int): ID del autor del libro.
        id_categoria (int): ID de la categoría del libro.
        id_subcategoria (int): ID de la subcategoría del libro.
        file (UploadFile, optional): Archivo del libro físico. Defaults to None.
        url_image (str, optional): URL de la imagen del libro físico. Defaults to None.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Raises:
        HTTPException: Se lanza si el usuario no es administrador o si falta la imagen o el archivo.
    Returns:
        dict: Mensaje indicando que el libro físico se creó correctamente.
    """
    if file is None and url_image is None:
        raise HTTPException(status_code=400, detail="You need to upload a file or url_image")
    exist = exist_physicalBook(titulo, id_autor, db)
    if exist:
        raise HTTPException(status_code=400, detail="Physical book already exist")
    book = await register_physicalBook(titulo,descripcion,ubicacion,estado, id_autor, id_categoria, id_subcategoria,file,url_image)
    
    new_book = create_physicalBook(book,db)
    #return PhysicalBook(**new_book.__dict__)
    return {"message": "Physical book created successfully"}

#obtener libro fisico por titulo
@router.get("/book/{titulo}/{id_author}", dependencies=[Depends(Portador())])
def get_physicalBook(titulo: str, id_author: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener los detalles de un libro físico por título y ID de autor.
    Args:
        titulo (str): Título del libro físico.
        id_author (int): ID del autor del libro.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Detalles del libro físico o mensaje indicando que el libro no existe.
    """
    exist = exist_physicalBook(titulo, id_author, db)
    if not exist:
        return {"message": "Physical book not exist"}
    
    return PhysicalBookOut(**exist.__dict__)

#obtener todos los libros fisicos
@router.get("/all_physicalBooks/", response_model=list[PhysicalBookOut])
def get_all_physicalBook(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los libros físicos.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        list: Lista de libros físicos o mensaje indicando que no hay libros.
    """
    return all_physicalBook(db)

#eliminar libro fisico por id
@router.delete("/delete_physicalBook/{id}")
def delete_physicalBookk(id: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar un libro físico por ID.
    Args:
        id (int): ID del libro físico.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Mensaje indicando que el libro físico se eliminó correctamente o que no existe.
    """
    physicalBookDeleted = delete_physicalBook(id, db)
    if not physicalBookDeleted:
        return {"message": "Physical book not exist"}
    return {"message": "Physical book deleted successfully"}
    

@router.get("/search_physicalBook/")
def search_physical_book_endpoint(titulo: str = None, categoria: str = None, subcategoria: str = None, 
                                 autor: str = None, db: Session = Depends(get_db)):
    """
    Endpoint para buscar libros físicos según diferentes criterios.
    Args:
        titulo (str, optional): Título del libro físico. Defaults to None.
        categoria (str, optional): Categoría del libro físico. Defaults to None.
        subcategoria (str, optional): Subcategoría del libro físico. Defaults to None.
        autor (str, optional): Autor del libro físico. Defaults to None.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Lista de libros físicos encontrados o mensaje indicando que no se encontraron libros.
    """
    physicalBooks = search_physical_book(titulo, categoria, subcategoria, autor, db)
    if not physicalBooks:
        return {"message": "No physical books found with the criteria provided"}
    
    return physicalBooks 

@router.put("/update_physicalBook/{physicalBook_id}", dependencies=[Depends(Portador())])
def update_physicalBookk(physicalBook_id: int, physicalBook: PhysicalBook, db: Session = Depends(get_db)):
    updated_physicalBook = update_physicalbook(physicalBook_id, physicalBook, db)
    if not updated_physicalBook:
        return {"message": "Physical book not exist"}
    return updated_physicalBook

