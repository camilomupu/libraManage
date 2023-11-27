
from fastapi import APIRouter, Depends, File, UploadFile, File, Request
from fastapi.responses import FileResponse
from typing import List
import requests
from schemas.physicalBook import PhysicalBook, PhysicalBookOut
from config.db import get_db, upload_file
from sqlalchemy.orm import Session
from controllers.physicalBook import create_physicalBook, exist_physicalBook, all_physicalBook, delete_physicalBook, exist_user_admin
from controllers.author import get_author
from controllers.category import get_category
from controllers.subcategory import get_subcategory

router = APIRouter()

#nuevo libro fisico
@router.post("/new_physicalBook/")
def create_new_physicalBook(book: PhysicalBook, db: Session = Depends(get_db)):
    exist = exist_physicalBook(book.titulo, book.id_autor, db)
    if exist:
        return {"message": "Physical book already exist"}
    if not get_author(book.id_autor, db):
        return {"message": "Author not exist"}
    if not get_category(book.id_categoria, db):
        return {"message": "Category not exist"}
    if not get_subcategory(book.id_subcategoria, db):
        return {"message": "Subcategory not exist"}
    new_physicalBook = create_physicalBook(book,db)
    return PhysicalBook(**new_physicalBook.__dict__)

#obtener libro fisico por titulo
@router.get("/book/{titulo}/{id_author}")
def get_physicalBook(titulo: str, id_author: int, db: Session = Depends(get_db)):
    exist = exist_physicalBook(titulo, id_author, db)
    if not exist:
        return {"message": "Physical book not exist"}
    
    return PhysicalBookOut(**exist.__dict__)

#obtener todos los libros fisicos
@router.get("/all_physicalBooks/", response_model=list[PhysicalBook])
def get_all_physicalBook(db: Session = Depends(get_db)):
    return all_physicalBook(db)

#eliminar libro fisico por id
@router.delete("/delete_physicalBook/{id}")
def delete_physicalBookk(id: int, db: Session = Depends(get_db)):
    physicalBookDeleted = delete_physicalBook(id, db)
    if not physicalBookDeleted:
        return {"message": "Physical book not exist"}
    return {"message": "Physical book deleted successfully", 
            "physical book": PhysicalBook(**physicalBookDeleted.__dict__)}
    

#Ruta para registrar los libros fisicos
@router.post("/register_physicalBook/")
async def register_physicalBook(book:PhysicalBook, correo:str, file: UploadFile=File(...), db: Session = Depends(get_db)):
   
    if exist_user_admin(correo,db):
        exist = exist_physicalBook(book.titulo, db)
        if exist:
            return {"message": "Physical book already exist"}
        url_imagen = await upload_file(file)
        #Asociamos la url de la imagen al libro
        book.imagen = url_imagen
        new_physicalBook = create_physicalBook(book,db)
        return PhysicalBook(**new_physicalBook.__dict__)
    return {"message": "You are not admin"}



