from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.physicalBook import search_physical_book
from controllers.digitalBook import search_digital_book


router = APIRouter()

@router.get("/search_book/")
def search_physical_book_endpoint(titulo: str = None, categoria: str = None, subcategoria: str = None, 
                                 autor: str = None, db: Session = Depends(get_db)):
    
    physicalBooks = search_physical_book(titulo, categoria, subcategoria, autor, db)
    digitalBooks = search_digital_book(titulo, categoria, subcategoria, autor, db)
    
    if not physicalBooks and not digitalBooks:
        return {"message": "No books found with the criteria provided"}
    
    physicalBooks.extend(digitalBooks)    
    return physicalBooks 