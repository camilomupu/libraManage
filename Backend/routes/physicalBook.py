
from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from schemas.physicalBook import PhysicalBook, PhysicalBookOut
from config.db import get_db, upload_img
from sqlalchemy.orm import Session
from controllers.physicalBook import create_physicalBook, exist_physicalBook, all_physicalBook, delete_physicalBook, exist_user_admin, search_physical_book,register_physicalBook
from controllers.author import get_author
from controllers.category import get_category
from controllers.subcategory import get_subcategory


router = APIRouter()

#nuevo libro fisico
"""@router.post("/new_physicalBook/")
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
    return PhysicalBook(**new_physicalBook.__dict__)"""
    
@router.post("/register_physicalBooks/")
async def register_physicalBooks(correo:str,titulo:str,descricion:str,ubicacion:str,
                  estado:str, id_autor:int, id_categoria:int, id_subcategoria:int
                  , file: UploadFile = None, url_image:str = None, db: Session = Depends(get_db)):
    if not exist_user_admin(correo,db):
        raise HTTPException(status_code=400, detail="You are not admin")
    if file is None and url_image is None:
        raise HTTPException(status_code=400, detail="You need to upload a file or url_image")
    exist = exist_physicalBook(titulo, id_autor, db)
    if exist:
        raise HTTPException(status_code=400, detail="Physical book already exist")
    book = await register_physicalBook(titulo,descricion,ubicacion,estado, id_autor, id_categoria, id_subcategoria,file,url_image)
    
    new_book = create_physicalBook(book,db)
    #return PhysicalBook(**new_book.__dict__)
    return {"message": "Physical book created successfully"}

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
    
"""
@router.post("/upload_image/{correo}/")
async def upload_images(correo:str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not exist_user_admin(correo,db):
        raise HTTPException(status_code=400, detail="You are not admin")
    url_archivo_subido = await upload_img(file)
    return url_archivo_subido
"""

    

"""

@router.post("/register_physicalBook/{correo}/{ruta_imagen}/")
async def register_physicalBook(book:PhysicalBook, correo:str,  db: Session = Depends(get_db)):
    if exist_user_admin(correo,db):
        exist = exist_physicalBook(book.titulo,book.id_autor , db)
        if exist:
            raise HTTPException(status_code=400, detail="Physical book already exist")
        
        new_physicalBook = create_physicalBook(book,db)
        return PhysicalBook(**new_physicalBook.__dict__)
    raise HTTPException(status_code=400, detail="You are not admin")


"""
@router.get("/search_physicalBook/")
def search_physical_book_endpoint(titulo: str = None, categoria: str = None, subcategoria: str = None, 
                                 autor: str = None, db: Session = Depends(get_db)):
    
    physicalBooks = search_physical_book(titulo, categoria, subcategoria, autor, db)
    if not physicalBooks:
        return {"message": "No physical books found with the criteria provided"}
    
    return physicalBooks 