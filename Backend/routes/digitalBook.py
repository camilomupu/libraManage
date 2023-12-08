#van a ir todas las rutas relacionadas con el digitalBook 
from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from schemas.digitalBook import DigitalBookCreate, DBookOut
from config.db import get_db, upload_img, upload_pdfs
from sqlalchemy.orm import Session
from controllers.digitalBook  import create_dBook, exist_dBook, all_dBooks, delete_dBook, exist_user_admin, search_digital_book, register_digitalBook


router = APIRouter()

#nuevo digitalBook 
"""@router.post("/new_digitalBook/")
def create_new_digital_book(digitalBook : DigitalBookCreate, db: Session = Depends(get_db)):
    exist = exist_dBook(digitalBook .titulo, digitalBook .id_autor, db)
    if exist:
        return {"message": "Digital book already exist"}
    new_user = create_dBook(digitalBook ,db)
    return DigitalBookCreate(**new_user.__dict__)"""
    
@router.post("/register_digitalBooks/")
async def register_digitalBooks(correo:str,titulo:str,descripcion:str, precio:str, id_autor:int, id_categoria:int, id_subcategoria:int
                  , file_img: UploadFile = None, file_pdf : UploadFile = None, url_image:str = None, link_libro:str=None,  db: Session = Depends(get_db)):
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
@router.get("/digitalBook/{title}/{id_autor}")
def get_digital_book(title: str ,id_autor: int, db: Session = Depends(get_db)):
    exist = exist_dBook(title, id_autor, db)
    if not exist:
        return {"message": "Digital book not exist"}
    
    return DBookOut(**exist.__dict__)
    

#obtener todos los digitalBook es
@router.get("/all_digitalBooks/", response_model=list[DBookOut])
def get_all_digital_books(db: Session = Depends(get_db)):
    return all_dBooks(db)

#eliminar digitalBook es por id
@router.delete("/delete_digitalBook/{id}")
def delete_digital_book(id: int, db: Session = Depends(get_db)):
    digitalBookDeleted = delete_dBook(id, db)
    if not digitalBookDeleted:
        return {"message": "Digital book not exist"}
    return {"message": "Digital book deleted successfully"}


"""@router.post("/upload_img_digitalBook/{correo}/")
async def upload_images_dBook(correo:str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not exist_user_admin(correo,db):
        raise HTTPException(status_code=400, detail="You are not admin")
    url_archivo_subido = await upload_img(file)
    return url_archivo_subido

@router.post("/upload_pdf_book/{correo}/")
async def upload_files(correo:str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not exist_user_admin(correo,db):
        raise HTTPException(status_code=400, detail="You are not admin")
    url_archivo_subido = await upload_pdfs(file)
    return url_archivo_subido"""



@router.get("/search_digitalBook/")
def search_digital_book_endpoint(titulo: str = None, categoria: str = None, subcategoria: str = None, 
                                 autor: str = None, db: Session = Depends(get_db)):
    
    digitalBooks = search_digital_book(titulo, categoria, subcategoria, autor, db)
    if not digitalBooks:
        return {"message": "No digital books were found with the criteria provided"}
    
    return digitalBooks