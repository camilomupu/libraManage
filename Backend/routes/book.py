from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.physicalBook import search_physical_book, all_physicalBook
from controllers.digitalBook import search_digital_book, all_dBooks


router = APIRouter()

@router.get("/all_books_general/")
def all_book_endpoint(db: Session = Depends(get_db)):
    
    physicalBooks = all_dBooks(db)
    digitalBooks = all_dBooks(db)
    
    if not physicalBooks and not digitalBooks:
        return {"message": "No books found"}
    
    physicalBooks.extend(digitalBooks)    
    return physicalBooks 

@router.get("/search_book/")
def search_book_endpoint(titulo: str = None, categoria: str = None, subcategoria: str = None, 
                                 autor: str = None, db: Session = Depends(get_db)):
    
    physicalBooks = search_physical_book(titulo, categoria, subcategoria, autor, db)
    digitalBooks = search_digital_book(titulo, categoria, subcategoria, autor, db)
    
    if not physicalBooks and not digitalBooks:
        return {"message": "No books found with the criteria provided"}
    
    physicalBooks.extend(digitalBooks)    
    return physicalBooks 