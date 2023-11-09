#van a ir todas las rutas relacionadas con el multa
from fastapi import APIRouter, Depends
from schemas.fine import Fine, MultaCreate
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.fine import create_author, exist_author, all_authors, delete_authors


router = APIRouter()

#nuevo multa
@router.post("/new_fine/")
def create_new_author(multa: MultaCreate, db: Session = Depends(get_db)):
    exist = exist_author(multa.id_multa, db)
    if exist:
        return {"message": "Fine already exist"}
    new_author = create_author(multa,db)
    return Fine(**new_author.__dict__)


#obtener multa por id_multa
@router.get("/{id_multa}")
def get_author(id_multa: int, db: Session = Depends(get_db)):
    exist = exist_author(id_multa, db)
    if not exist:
        return {"message": "Fine not exist"}
    
    return Fine(**exist.__dict__)
    

#obtener todos los multas
@router.get("/all/", response_model=list[Fine])
def get_all_authors(db: Session = Depends(get_db)):
    return all_authors(db)

#eliminar multas por id_multa
@router.delete("/delete/{id_multa}")
def delete_author(id_multa: str, db: Session = Depends(get_db)):
    authorDeleted = delete_authors(id_multa, db)
    if not authorDeleted:
        return {"message": "Fine not exist"}
    return {"message": "Fine deleted successfully", "fine": Fine(**authorDeleted.__dict__)}