from fastapi import APIRouter, Depends
from schemas.category import Category, CategoryOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.category import create_category, exist_category, all_categories, delete_categories
from routes.user import Portador

router = APIRouter()

#nueva categoria
@router.post("/new_category/", dependencies=[Depends(Portador())])
def create_new_category(categoria: Category, db: Session = Depends(get_db)):
    exist = exist_category(categoria.nombre, db)
    if exist:
        return {"message": "Categoria already exist"}
    new_categoria = create_category(categoria,db)
    return CategoryOut(**new_categoria.__dict__)

#obtener categoria por nombre
@router.get("/category/{nombre}", dependencies=[Depends(Portador())])
def get_categoria(nombre: str, db: Session = Depends(get_db)):
    exist = exist_category(nombre, db)
    if not exist:
        return {"message": "Categoria not exist"}
    
    return CategoryOut(**exist.__dict__)

#obtener todas las categorias
@router.get("/all_categories/", response_model=list[CategoryOut])
def get_all_categorias(db: Session = Depends(get_db)):
    return all_categories(db)

#eliminar categorias por id
@router.delete("/delete_categories/{id}", dependencies=[Depends(Portador())])
def delete_categoria(id: int, db: Session = Depends(get_db)):
    categoriaDeleted = delete_categories(id, db)
    if not categoriaDeleted:
        return {"message": "Categoria not exist"}
    return {"message": "Categoria deleted successfully", "categoria": Category(**categoriaDeleted.__dict__)}