#van a ir todas las rutas relacionadas con el digitalBook 
from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from schemas.digitalBook import DigitalBookCreate, DBookOut
from config.db import get_db, upload_img, upload_pdfs
from sqlalchemy.orm import Session
from controllers.digitalBook  import create_dBook, exist_dBook, all_dBooks, delete_dBook, exist_user_admin, search_digital_book, register_digitalBook
from routes.user import Portador

router = APIRouter()
    
@router.post("/register_digitalBooks/", dependencies=[Depends(Portador())])
async def register_digitalBooks(correo:str,titulo:str,descripcion:str, precio:str, id_autor:int, id_categoria:int, id_subcategoria:int
                  , file_img: UploadFile = None, file_pdf : UploadFile = None, url_image:str = None, link_libro:str=None,  db: Session = Depends(get_db)):
    """
    Registra un nuevo libro digital en la base de datos.
    Args:
        correo (str): Correo electrónico del usuario administrador.
        titulo (str): Título del libro digital.
        descripcion (str): Descripción del libro digital.
        precio (str): Precio del libro digital.
        id_autor (int): ID del autor del libro digital.
        id_categoria (int): ID de la categoría del libro digital.
        id_subcategoria (int): ID de la subcategoría del libro digital.
        file_img (UploadFile): Archivo de imagen del libro digital (opcional).
        file_pdf (UploadFile): Archivo PDF del libro digital (opcional).
        url_image (str): URL de la imagen del libro digital (opcional).
        link_libro (str): URL del libro digital (opcional).
        db (Session): Sesión de la base de datos.
    Raises:
        HTTPException: Se eleva una excepción si el usuario no es administrador, no se proporciona un archivo o URL de imagen,
        o no se proporciona un archivo PDF o URL del libro.
    Returns:
        dict: Mensaje indicando que el libro digital se creó exitosamente.
    """
    if not exist_user_admin(correo,db):
        raise HTTPException(status_code=400, detail="You are not admin")
    if file_img is None and url_image is None:
        raise HTTPException(status_code=400, detail="You need to upload a file or url_image")
    if file_pdf is None and link_libro is None:
        raise HTTPException(status_code=400, detail="You need to upload a file or url_pdf")
    
    exist = exist_dBook(titulo,id_autor , db)
    if exist:
        raise HTTPException(status_code=400, detail="Digital book already exist")
    book = await register_digitalBook(titulo,descripcion, precio, id_autor, id_categoria, id_subcategoria,file_img,file_pdf,url_image,link_libro)
    new_book = create_dBook(book,db)
    #return DigitalBookCreate(**new_book.__dict__)
    return {"message": "Digital book created successfully"}


#obtener digitalBook  por correo
@router.get("/digitalBook/{title}/{id_autor}", dependencies=[Depends(Portador())])
def get_digital_book(title: str ,id_autor: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de un libro digital por su título y ID de autor.
    Args:
        title (str): Título del libro digital.
        id_autor (int): ID del autor del libro digital.
        db (Session): Sesión de la base de datos.
    Returns:
        DBookOut or dict: Detalles del libro digital si existe.
        Mensaje indicando que el libro digital no existe si no se encuentra.
    """
    exist = exist_dBook(title, id_autor, db)
    if not exist:
        return {"message": "Digital book not exist"}
    
    return DBookOut(**exist.__dict__)
    

#obtener todos los digitalBook es
@router.get("/all_digitalBooks/", response_model=list[DBookOut])
def get_all_digital_books(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los libros digitales.
    Args:
        db (Session): Sesión de la base de datos.
    Returns:
        list[DBookOut]: Lista de libros digitales.
    """
    return all_dBooks(db)

#eliminar digitalBook es por id
@router.delete("/delete_digitalBook/{id}", dependencies=[Depends(Portador())])
def delete_digital_book(id: int, db: Session = Depends(get_db)):
    """
    Elimina un libro digital por su ID.
    Args:
        id (int): ID del libro digital.
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando si el libro digital se eliminó exitosamente o si no existe.
    """
    digitalBookDeleted = delete_dBook(id, db)
    if not digitalBookDeleted:
        return {"message": "Digital book not exist"}
    return {"message": "Digital book deleted successfully"}


@router.get("/search_digitalBook/")
def search_digital_book_endpoint(titulo: str = None, categoria: str = None, subcategoria: str = None, 
                                 autor: str = None, db: Session = Depends(get_db)):
    """
    Endpoint para buscar libros digitales con criterios específicos.
    Args:
        titulo (str): Título del libro digital (opcional).
        categoria (str): Nombre de la categoría del libro digital (opcional).
        subcategoria (str): Nombre de la subcategoría del libro digital (opcional).
        autor (str): Nombre del autor del libro digital (opcional).
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Lista de libros digitales que coinciden con los criterios proporcionados o un mensaje indicando que no se encontraron libros.
    """
    digitalBooks = search_digital_book(titulo, categoria, subcategoria, autor, db)
    if not digitalBooks:
        return {"message": "No digital books were found with the criteria provided"}
    
    return digitalBooks