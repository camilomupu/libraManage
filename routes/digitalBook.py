#van a ir todas las rutas relacionadas con el digitalBook 
from fastapi import APIRouter, Depends
from schemas.digitalBook import DigitalBookCreate, DBookOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.digitalBook  import create_dBook, exist_dBook, all_dBooks, delete_dBook


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
    
    return DigitalBookCreate(**exist.__dict__)
    

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
    return {"message": "Digital book deleted successfully", "Digital book": DigitalBookCreate(**digitalBookDeleted.__dict__)}