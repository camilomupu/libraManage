from fastapi import APIRouter, Depends
from schemas.subcategory import SubCategory, SubCategoryOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.subcategory import create_subcategory, exist_subcategory, all_subcategories, delete_subcategories
from routes.user import Portador


router = APIRouter()

#nueva subcategoria
@router.post("/new_subcategory/", dependencies=[Depends(Portador())])
def create_new_subcategory(subcategoria: SubCategory, db: Session = Depends(get_db)):
    exist = exist_subcategory(subcategoria.nombre, db)
    if exist:
        return {"message": "Subcategoria already exist"}
    new_subcategoria = create_subcategory(subcategoria,db)
    #return SubCategory(**new_subcategoria.__dict__)
    return {"message": "Subcategoria created successfully"}

#obtener subcategoria por nombre
@router.get("/subcategory/{nombre}", dependencies=[Depends(Portador())])
def get_subcategory(nombre: str, db: Session = Depends(get_db)):
    exist = exist_subcategory(nombre, db)
    if not exist:
        return {"message": "Subcategoria not exist"}
    
    return SubCategoryOut(**exist.__dict__)

#obtener todas las subcategorias
@router.get("/all_subcategories/", response_model=list[SubCategoryOut])
def get_all_subcategories(db: Session = Depends(get_db)):
    return all_subcategories(db)

#eliminar subcategorias por id  
@router.delete("/delete_subcategories/{id}")
def delete_subcategories(id: int, db: Session = Depends(get_db)):
    subcategoriaDeleted = delete_subcategories(id, db)
    if not subcategoriaDeleted:
        return {"message": "Subcategoria not exist"}
    return {"message": "Subcategoria deleted successfully", "subcategoria": SubCategory(**subcategoriaDeleted.__dict__)}