from schemas.digitalBook import DigitalBookCreate
from models.tables import *
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from config.db import upload_img, upload_pdfs
from sqlalchemy.exc import NoResultFound

def create_dBook(nuevo_dBook: DigitalBookCreate, db):
    """
    Crea un nuevo libro digital en la base de datos.
    Args:
        nuevo_dBook (DigitalBookCreate): Objeto que contiene la información del nuevo libro digital.
        db: Sesión de la base de datos.
    Returns:
        LibroDigital: El objeto LibroDigital recién creado.
    """
    libro = LibroDigital(**nuevo_dBook.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro

def exist_dBook(title: str, id_autor: int, db):
    """
    Verifica si existe un libro digital con el título y autor especificados en la base de datos.
    Args:
        title (str): Título del libro digital.
        id_autor (int): ID del autor del libro digital.
        db: Sesión de la base de datos.
    Returns:
        LibroDigital or None: El objeto LibroDigital si existe, None si no se encuentra.
    """
    libro = db.query(LibroDigital).filter((LibroDigital.titulo == title) & (LibroDigital.id_autor == id_autor)).first()
    return libro

def get_dBook(id: int, db):
    """
    Obtiene un libro digital por su ID.
    Args:
        id (int): ID del libro digital a recuperar.
        db: Sesión de la base de datos.
    Returns:
        LibroDigital or None: El objeto LibroDigital si se encuentra, None si no se encuentra.
    """
    libro = db.query(LibroDigital).filter(LibroDigital.id == id).first()
    return libro

def all_dBooks(db):
    """
    Obtiene todos los registros de libros digitales en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        List[LibroDigital]: Lista que contiene todos los registros de LibroDigital.
    """
    return db.query(LibroDigital).all()

def delete_dBook(id: int, db):
    """
    Elimina un libro digital por su ID.
    Args:
        id (int): ID del libro digital a eliminar.
        db: Sesión de la base de datos.
    Returns:
        LibroDigital or None: El objeto LibroDigital eliminado si se encuentra, None si no se encuentra.
    """
    try:
        libro = db.query(LibroDigital).filter(LibroDigital.id == id).one()
        db.delete(libro)
        db.commit()
        return libro
    except NoResultFound:
        db.rollback()
        return None

def exist_user_admin(correo:str, db): #Verificamos si el usuario es administrador
    """
    Verifica si el usuario con el correo especificado es un administrador.
    Args:
        correo (str): Correo electrónico del usuario.
        db: Sesión de la base de datos.
    Returns:
        bool: True si el usuario es administrador, False en caso contrario.
    """
    user = db.query(Usuario).filter(Usuario.correo == correo).first()
    if user is None: #Verificamos si el usuario existe
        return False
    if user.id_rol is None: #Verificamos si el usuario tiene rol
        return False
    rol = db.query(Rol).filter(Rol.id == user.id_rol).first()

    if rol is None: #Verificamos si el rol existe
        return False
    if rol.nombre == "Administrador" or rol.nombre == "administrador": #Verificamos si el rol es administrador
        return True
    return False

async def register_digitalBook(titulo:str,descripcion:str, precio:str, id_autor:int, id_categoria:int, id_subcategoria:int
                  , file_img: UploadFile = None, file_pdf : UploadFile = None, url_image:str = None,
                  link_libro:str=None):
    """
    Registra un nuevo libro digital, obteniendo las URLs de las imágenes y los archivos PDF.
    Args:
        titulo (str): Título del libro digital.
        descripcion (str): Descripción del libro digital.
        precio (str): Precio del libro digital.
        id_autor (int): ID del autor del libro digital.
        id_categoria (int): ID de la categoría del libro digital.
        id_subcategoria (int): ID de la subcategoría del libro digital.
        file_img (UploadFile): Archivo de imagen para la portada del libro digital.
        file_pdf (UploadFile): Archivo PDF del libro digital.
        url_image (str): URL de la imagen del libro digital.
        link_libro (str): URL del libro digital.
    Returns:
        DigitalBookCreate: Objeto con la información del nuevo libro digital.
    """
    if file_img is not None:
        url_img = await upload_img(file_img)
    else:
        url_img = url_image
    if url_img is None:
        raise ValueError("Se requiere una imagen (file o url_imagen) para crear el libro digital.")
    if file_pdf is not None:
        url_pdf = await upload_pdfs(file_pdf)
    else:
        url_pdf = link_libro
    if url_pdf is None:
        raise ValueError("Se requiere un pdf (file o url_pdf) para crear el libro digital.")
    
    new_digitalBook = DigitalBookCreate(titulo=titulo, portada=url_img, link_Libro=url_pdf, descripcion = descripcion,
                                        precio = precio,id_autor=id_autor, id_subcategoria=id_subcategoria, 
                                        id_categoria=id_categoria,)
    return new_digitalBook

def search_digital_book(titulo: str = None, categoria: str = None, subcategoria: str = None, autor: str = None, db: Session = None):
    query = db.query(LibroDigital)
    """
    Realiza una búsqueda de libros digitales en la base de datos con los criterios especificados.
    Args:
        titulo (str): Título del libro digital a buscar.
        categoria (str): Categoría del libro digital a buscar.
        subcategoria (str): Subcategoría del libro digital a buscar.
        autor (str): Autor del libro digital a buscar.
        db: Sesión de la base de datos.
    Returns:
        List[LibroDigital]: Lista de libros digitales que cumplen con los criterios de búsqueda.
    """
    if titulo:
        titulo = titulo.strip()  # Elimina espacios al inicio y al final
        query = query.filter(func.upper(LibroDigital.titulo).contains(titulo.upper()))
    if categoria:
        categoria = categoria.strip()
        query = query.join(Categoria).filter(func.upper(Categoria.nombre) == categoria.upper())
    if subcategoria:
        subcategoria = subcategoria.strip()
        query = query.join(SubCategoria).filter(func.upper(SubCategoria.nombre) == subcategoria.upper())
    if autor:
        autor = autor.strip()
        query = query.join(Autor).filter(func.upper(Autor.nombre).contains(autor.upper()))

    digitalBooks = query.all()
    return digitalBooks