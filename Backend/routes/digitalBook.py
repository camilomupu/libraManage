#van a ir todas las rutas relacionadas con el digitalBook 
from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from schemas.digitalBook import DigitalBookCreate, DBookOut
from config.db import get_db, upload_img, upload_pdfs
from sqlalchemy.orm import Session
from controllers.digitalBook  import create_dBook, exist_dBook, all_dBooks, delete_dBook, exist_user_admin


router = APIRouter()

#nuevo digitalBook 
@router.post("/new_digitalBook/")
def create_new_digital_book(digitalBook : DigitalBookCreate, db: Session = Depends(get_db)):
    exist = exist_dBook(digitalBook .titulo, digitalBook .id_autor, db)
    if exist:
        return {"message": "Digital book already exist"}
    new_user = create_dBook(digitalBook ,db)
    return DigitalBookCreate(**new_user.__dict__)


#obtener digitalBook  por correo
@router.get("/digitalBook/{title}/{id_autor}")
def get_digital_book(title: str ,id_autor: int, db: Session = Depends(get_db)):
    exist = exist_dBook(title, id_autor, db)
    if not exist:
        return {"message": "Digital book not exist"}
    
    return DBookOut(**exist.__dict__)
    

#obtener todos los digitalBook es
@router.get("/all_digitalBooks/", response_model=list[DigitalBookCreate])
def get_all_digital_books(db: Session = Depends(get_db)):
    return all_dBooks(db)

#eliminar digitalBook es por id
@router.delete("/delete_digitalBook/{id}")
def delete_digital_book(id: int, db: Session = Depends(get_db)):
    digitalBookDeleted = delete_dBook(id, db)
    if not digitalBookDeleted:
        return {"message": "Digital book not exist"}
    return {"message": "Digital book deleted successfully", "Digital book": DigitalBookCreate(**digitalBookDeleted.__dict__)}


@router.post("/upload_img_digitalBook/{correo}/")
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
    return url_archivo_subido

@router.post("/register_digitalBook/{correo}/{ruta_imagen}/{ruta_libro}/")
async def register_digitalBook(book:DigitalBookCreate, correo:str, url_img:str, link_libr:str,  db: Session = Depends(get_db)):
    if exist_user_admin(correo,db):
        exist = exist_dBook(book.titulo,book.id_autor , db)
        if exist:
            raise HTTPException(status_code=400, detail="Digital book already exist")
        book.portada = url_img
        book.link_libro = link_libr
        new_digitalBook = create_dBook(book,db)
        return DigitalBookCreate(**new_digitalBook.__dict__)
    raise HTTPException(status_code=400, detail="You are not admin")