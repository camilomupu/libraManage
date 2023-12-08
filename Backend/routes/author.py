from fastapi import APIRouter, Depends
from schemas.author import Author, AuthorOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.author import create_author, exist_author, all_authors, delete_authors
from routes.user import Portador


router = APIRouter()

#nueva author
@router.post("/new_author/", dependencies=[Depends(Portador())])
def create_new_author(author: Author, db: Session = Depends(get_db)):
    exist = exist_author(author.nombre, db)
    if exist:
        return {"message": "author already exist"}
    new_author = create_author(author,db)
    return Author(**new_author.__dict__)

#obtener author por nombre
@router.get("/author/{nombre}", dependencies=[Depends(Portador())])
def get_author(nombre: str, db: Session = Depends(get_db)):
    exist = exist_author(nombre, db)
    if not exist:
        return {"message": "author not exist"}
    
    return AuthorOut(**exist.__dict__)

#obtener todas las authors
@router.get("/all_authors/", response_model=list[Author], dependencies=[Depends(Portador())])
def get_all_authors(db: Session = Depends(get_db)):
    return all_authors(db)

#eliminar authors por id  
@router.delete("/delete_authors/{id}", dependencies=[Depends(Portador())])
def delete_authorss(id: int, db: Session = Depends(get_db)):
    authorDeleted = delete_authors(id, db)
    if not authorDeleted:
        return {"message": "author not exist"}
    return {"message": "author deleted successfully"}