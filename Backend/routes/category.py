from fastapi import APIRouter, Depends
from schemas.category import Category, CategoryOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.category import create_category, exist_category, all_categories, delete_categories, update_category
from routes.user import Portador

router = APIRouter()

#nueva categoria
@router.post("/new_category/")
def create_new_category(categoria: Category, db: Session = Depends(get_db)):
    """
    Crea una nueva categoría.
    Args:
        categoria (Category): Datos de la nueva categoría.
        db (Session): Sesión de la base de datos.
    Returns:
        CategoryOut or dict: Detalles de la categoría creada si no existe una categoría con el mismo nombre.
        Mensaje indicando que la categoría ya existe si ya hay una categoría con el mismo nombre.
    """
    exist = exist_category(categoria.nombre, db)
    if exist:
        return {"message": "Categoria already exist"}
    new_categoria = create_category(categoria,db)
    return CategoryOut(**new_categoria.__dict__)

#obtener categoria por nombre
@router.get("/category/{nombre}", dependencies=[Depends(Portador())])
def get_categoria(nombre: str, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una categoría por su nombre.
    Args:
        nombre (str): Nombre de la categoría.
        db (Session): Sesión de la base de datos.
    Returns:
        CategoryOut or dict: Detalles de la categoría si existe.
        Mensaje indicando que la categoría no existe si no se encuentra.
    """
    exist = exist_category(nombre, db)
    if not exist:
        return {"message": "Categoria not exist"}
    
    return CategoryOut(**exist.__dict__)

#obtener todas las categorias
@router.get("/all_categories/", response_model=list[CategoryOut])
def get_all_categorias(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todas las categorías.
    Args:
        db (Session): Sesión de la base de datos.
    Returns:
        list[CategoryOut]: Lista de categorías.
    """
    return all_categories(db)

#eliminar categorias por id
@router.delete("/delete_categories/{id}")
def delete_categoria(id: int, db: Session = Depends(get_db)):
    """
    Elimina una categoría por su ID.
    Args:
        id (int): ID de la categoría.
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando si la categoría se eliminó exitosamente o si no existe.
    """
    categoriaDeleted = delete_categories(id, db)
    if not categoriaDeleted:
        return {"message": "Categoria not exist"}
    return {"message": "Categoria deleted successfully", "categoria": Category(**categoriaDeleted.__dict__)}

@router.put("/update_category/{category_id}", dependencies=[Depends(Portador())])
def update_categoria(category_id: int, categoria: Category, db: Session = Depends(get_db)):
    updated_categoria = update_category(category_id, categoria, db)
    if not updated_categoria:
        return {"message": "Categoria not exist"}
    return updated_categoria

