from fastapi import APIRouter, Depends
from schemas.physicalBook import PhysicalBook, PhysicalBookOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.physicalBook import create_physicalBook, exist_physicalBook, all_physicalBook, delete_physicalBook

router = APIRouter()

#nuevo libro fisico
@router.post("/new_physicalBook/")
def create_new_physicalBook(book: PhysicalBook, db: Session = Depends(get_db)):
    exist = exist_physicalBook(book.titulo, db)
    if exist:
        return {"message": "Physical book already exist"}
    new_physicalBook = create_physicalBook(book,db)
    return PhysicalBook(**new_physicalBook.__dict__)

#obtener libro fisico por titulo
@router.get("/book/{titulo}")
def get_physicalBook(titulo: str, db: Session = Depends(get_db)):
    exist = exist_physicalBook(titulo, db)
    if not exist:
        return {"message": "Physical book not exist"}
    
    return PhysicalBookOut(**exist.__dict__)

#obtener todos los libros fisicos
@router.get("/all_physicalBooks/", response_model=list[PhysicalBook])
def get_all_physicalBook(db: Session = Depends(get_db)):
    return all_physicalBook(db)

#eliminar libro fisico por id
@router.delete("/delete_physicalBook/{id}")
def delete_physicalBook(id: int, db: Session = Depends(get_db)):
    physicalBookDeleted = delete_physicalBook(id, db)
    if not physicalBookDeleted:
        return {"message": "Physical book not exist"}
    return {"message": "Physical book deleted successfully", "physical book": PhysicalBook(**physicalBookDeleted.__dict__)}