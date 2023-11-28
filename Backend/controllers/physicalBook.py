from schemas.physicalBook import PhysicalBook
from models.tables import *
from sqlalchemy import func, text
from sqlalchemy.orm import Session, joinedload

def create_physicalBook(new_book: PhysicalBook, db):
    book = LibroFisico(**new_book.__dict__)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def exist_physicalBook(titulo: str, id_author: int, db):
    book = db.query(LibroFisico).filter((func.upper(LibroFisico.titulo) == titulo.upper()) & (LibroFisico.id_autor == id_author)).first()
    return book

def get_physicalBook(id: int, db):
    book = db.query(LibroFisico).filter(LibroFisico.id == id).first()
    return book

def all_physicalBook(db):
    return db.query(LibroFisico).all()

def delete_physicalBook(id: int, db):
    book = db.query(LibroFisico).filter(LibroFisico.id == id).first()
    db.delete(book)
    db.commit()
    max_id = db.query(func.max(LibroFisico.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE librosFisicos_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return book
    
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

def search_physical_book(titulo: str = None, categoria: str = None, subcategoria: str = None, autor: str = None, db: Session = None):
    query = db.query(LibroFisico)

    if titulo:
        titulo = titulo.strip()  # Elimina espacios al inicio y al final
        query = query.filter(func.upper(LibroFisico.titulo).contains(titulo.upper()))
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
