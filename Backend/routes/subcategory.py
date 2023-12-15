from fastapi import APIRouter, Depends
from schemas.subcategory import SubCategory, SubCategoryOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.subcategory import create_subcategory, exist_subcategory, all_subcategories, delete_subcategories
from routes.user import Portador


router = APIRouter()

#nueva subcategoria
@router.post("/new_subcategory/")
def create_new_subcategory(subcategoria: SubCategory, db: Session = Depends(get_db)):
    """
    Endpoint para crear una nueva subcategoría.
    Args:
        subcategoria (SubCategory): Datos de la nueva subcategoría.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Mensaje indicando que la subcategoría se creó correctamente o que ya existe.
    """
    exist = exist_subcategory(subcategoria.nombre, db)
    if exist:
        return {"message": "Subcategoria already exist"}
    new_subcategoria = create_subcategory(subcategoria,db)
    #return SubCategory(**new_subcategoria.__dict__)
    return {"message": "Subcategoria created successfully"}

#obtener subcategoria por nombre
@router.get("/subcategory/{nombre}", dependencies=[Depends(Portador())])
def get_subcategory(nombre: str, db: Session = Depends(get_db)):
    """
    Endpoint para obtener una subcategoría por su nombre.
    Args:
        nombre (str): Nombre de la subcategoría.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        SubCategoryOut: Detalles de la subcategoría.
    """
    exist = exist_subcategory(nombre, db)
    if not exist:
        return {"message": "Subcategoria not exist"}
    
    return SubCategoryOut(**exist.__dict__)

#obtener todas las subcategorias
@router.get("/all_subcategories/", response_model=list[SubCategoryOut])
def get_all_subcategories(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todas las subcategorías.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        List[SubCategoryOut]: Lista de subcategorías.
    """
    return all_subcategories(db)

#eliminar subcategorias por id  
@router.delete("/delete_subcategories/{id}")
def delete_subcategories_endpoint(id: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar una subcategoría por su ID.
    Args:
        id (int): ID de la subcategoría.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Mensaje indicando que la subcategoría se eliminó correctamente o que no existe.
    """
    subcategoriaDeleted = delete_subcategories(id, db)
    if not subcategoriaDeleted:
        return {"message": "Subcategoria not exist"}
    return {"message": "Subcategoria deleted successfully", "subcategoria": SubCategory(**subcategoriaDeleted.__dict__)}