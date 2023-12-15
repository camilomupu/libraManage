from schemas.digitalBook import DigitalBookCreate
from models.tables import *
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from config.db import upload_img, upload_pdfs
from sqlalchemy.exc import NoResultFound
from typing import List, Optional

def create_dBook(nuevo_dBook: DigitalBookCreate, db):
    libro = LibroDigital(**nuevo_dBook.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro

def exist_dBook(title: str, id_autor: int, db):
    libro = db.query(LibroDigital).filter((LibroDigital.titulo == title) & (LibroDigital.id_autor == id_autor)).first()
    return libro

def get_dBook(id: int, db):
    libro = db.query(LibroDigital).filter(LibroDigital.id == id).first()
    return libro

def all_dBooks(db):
    return db.query(LibroDigital).all()

def delete_dBook(id: int, db):
    try:
        libro = db.query(LibroDigital).filter(LibroDigital.id == id).one()
        db.delete(libro)
        db.commit()
        return libro
    except NoResultFound:
        db.rollback()
        return None

def exist_user_admin(correo:str, db): #Verificamos si el usuario es administrador
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

async def register_digitalBook(titulo:str,descripcion:str, precio:float, id_autor:int, id_categoria:int, id_subcategoria:int
                  , file_img: UploadFile = None, file_pdf : UploadFile = None, url_image:str = None,
                  link_libro:str=None):
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
    
    new_digitalBook = DigitalBookCreate(titulo=titulo, portada=url_img, descripcion = descripcion, link_Libro=url_pdf, 
                                        precio = precio,id_autor=id_autor, id_subcategoria=id_subcategoria, 
                                        id_categoria=id_categoria,)
    return new_digitalBook

def search_digital_book(titulo: str = None, categoria: str = None, subcategoria: str = None, autor: str = None, db: Session = None):
    query = db.query(LibroDigital)

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

def get_digitalbookcreate(id: int, db):
    cat = db.query(LibroDigital).filter(LibroDigital.id == id).first()
    return cat


def update_digitalbookcreate(digitalbookcreate_id: int, updated_digitalbookcreate: DigitalBookCreate, db) -> Optional[DigitalBookCreate]:
        usr = get_digitalbookcreate(digitalbookcreate_id, db)
        if usr:
            usr.titulo = updated_digitalbookcreate.titulo
            usr.descripcion = updated_digitalbookcreate.descripcion
            usr.portada = updated_digitalbookcreate.portada
            usr.link_Libro = updated_digitalbookcreate.link_Libro
            usr.id_autor = updated_digitalbookcreate.id_autor
            usr.id_categoria = updated_digitalbookcreate.id_categoria
            usr.id_subcategoria = updated_digitalbookcreate.id_subcategoria
            usr.precio = updated_digitalbookcreate.precio
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None