#van a ir todas las rutas relacionadas con el fine
from fastapi import APIRouter, Depends
from schemas.fine import Fine, FineCreate
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.fine import create_fine, exist_fine, all_fines, delete_fines


router = APIRouter()

#nuevo fine
@router.post("/new_fine/")
def create_new_fine(fine: Fine, db: Session = Depends(get_db)):
    new_fine = create_fine(fine,db)
    return Fine(**new_fine.__dict__)


#obtener fine por id_fine
@router.get("/{id_fine}")
def get_fine(id_fine: int, db: Session = Depends(get_db)):
    exist = exist_fine(id_fine, db)
    if not exist:
        return {"message": "Fine not exist"}
    
    return Fine(**exist.__dict__)
    

#obtener todos los fines
@router.get("/all/", response_model=list[FineCreate])
def get_all_fines(db: Session = Depends(get_db)):
    return all_fines(db)

#eliminar fines por id_fine
@router.delete("/delete/{id_fine}")
def delete_fine(id_fine: str, db: Session = Depends(get_db)):
    fineDeleted = delete_fines(id_fine, db)
    if not fineDeleted:
        return {"message": "Fine not exist"}
    return {"message": "Fine deleted successfully", "fine": Fine(**fineDeleted.__dict__)}