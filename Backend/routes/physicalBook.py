
from fastapi import APIRouter, Depends, File, UploadFile, File, HTTPException
from schemas.physicalBook import PhysicalBook, PhysicalBookOut
from config.db import get_db, upload_img
from sqlalchemy.orm import Session
from controllers.physicalBook import create_physicalBook, exist_physicalBook, all_physicalBook, delete_physicalBook, exist_user_admin, search_physical_book,register_physicalBook
from controllers.author import get_author
from controllers.category import get_category
from controllers.subcategory import get_subcategory
from routes.user import Portador


router = APIRouter()

    
@router.post("/register_physicalBooks/", dependencies=[Depends(Portador())])
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
@router.get("/book/{titulo}/{id_author}", dependencies=[Depends(Portador())])
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
@router.delete("/delete_physicalBook/{id}", dependencies=[Depends(Portador())])
def delete_physicalBookk(id: int, db: Session = Depends(get_db)):
    physicalBookDeleted = delete_physicalBook(id, db)
    if not physicalBookDeleted:
        return {"message": "Physical book not exist"}
    return {"message": "Physical book deleted successfully", 
            "physical book": PhysicalBook(**physicalBookDeleted.__dict__)}
    

@router.get("/search_physicalBook/")
def search_physical_book_endpoint(titulo: str = None, categoria: str = None, subcategoria: str = None, 
                                 autor: str = None, db: Session = Depends(get_db)):
    
    physicalBooks = search_physical_book(titulo, categoria, subcategoria, autor, db)
    if not physicalBooks:
        return {"message": "No physical books found with the criteria provided"}
    
    return physicalBooks 