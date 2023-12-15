from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.physicalBook import search_physical_book, all_physicalBook
from controllers.digitalBook import search_digital_book, all_dBooks



router = APIRouter()

@router.get("/all_books_general/")
def all_book_endpoint(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los libros, tanto físicos como digitales, de la base de datos.
    Args:
        db (Session): Sesión de la base de datos.
    Returns:
        list[Union[LibroFisico, LibroDigital]] or dict: 
        Si hay libros, devuelve la lista de libros físicos y digitales.
        Si no hay libros, devuelve un mensaje indicando que no se encontraron libros.
    """
    physicalBooks = all_physicalBook(db)
    digitalBooks = all_dBooks(db)
    
    if not physicalBooks and not digitalBooks:
        return {"message": "No books found"}
    
    physicalBooks.extend(digitalBooks)    
    return physicalBooks 

@router.get("/search_book/")
def search_book_endpoint(titulo: str = None, categoria: str = None, subcategoria: str = None, 
                                 autor: str = None, db: Session = Depends(get_db)):
    """
    Busca libros en la base de datos según los criterios proporcionados.

    Args:
        titulo (str): Título del libro.
        categoria (str): Categoría del libro.
        subcategoria (str): Subcategoría del libro.
        autor (str): Autor del libro.
        db (Session): Sesión de la base de datos.

    Returns:
        list[Union[LibroFisico, LibroDigital]] or dict: 
        Si se encuentran libros, devuelve la lista de libros físicos y digitales que coinciden con los criterios.
        Si no se encuentran libros, devuelve un mensaje indicando que no se encontraron libros con los criterios proporcionados.
    """
    physicalBooks = search_physical_book(titulo, categoria, subcategoria, autor, db)
    digitalBooks = search_digital_book(titulo, categoria, subcategoria, autor, db)
    
    if not physicalBooks and not digitalBooks:
        return {"message": "No books found with the criteria provided"}
    
    physicalBooks.extend(digitalBooks)    
    return physicalBooks 