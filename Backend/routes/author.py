from fastapi import APIRouter, Depends
from schemas.author import Author, AuthorOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.author import create_author, exist_author, all_authors, delete_authors

router = APIRouter()

#nueva author
@router.post("/new_author/")
def create_new_author(author: Author, db: Session = Depends(get_db)):
    exist = exist_author(author.nombre, db)
    if exist:
        return {"message": "author already exist"}
    new_author = create_author(author,db)
    return Author(**new_author.__dict__)

#obtener author por nombre
@router.get("/author/{nombre}")
def get_author(nombre: str, db: Session = Depends(get_db)):
    exist = exist_author(nombre, db)
    if not exist:
        return {"message": "author not exist"}
    
    return AuthorOut(**exist.__dict__)

#obtener todas las authors
@router.get("/all_authors/", response_model=list[AuthorOut])
def get_all_authors(db: Session = Depends(get_db)):
    return all_authors(db)

#eliminar authors por id  
@router.delete("/delete_authors/{id}")
def delete_authors(id: int, db: Session = Depends(get_db)):
    authorDeleted = delete_authors(id, db)
    if not authorDeleted:
        return {"message": "author not exist"}
    return {"message": "author deleted successfully", "author": Author(**authorDeleted.__dict__)}