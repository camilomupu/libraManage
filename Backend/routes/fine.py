#van a ir todas las rutas relacionadas con el fine
from fastapi import APIRouter, Depends
from schemas.fine import Fine, FineCreate
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.fine import create_fine, add_fine_automatically, exist_fine, all_fines, delete_fines, delete_all_fines, forgive_fine, pay_fine
from routes.user import Portador

router = APIRouter()

#nuevo fine
@router.post("/new_fine/", dependencies=[Depends(Portador())])
def create_new_fine(fine: Fine, db: Session = Depends(get_db)):
    """
    Endpoint para crear una nueva multa.
    Args:
        fine (Fine): Datos de la multa.
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando que la multa se creó correctamente.
    """
    new_fine = create_fine(fine,db)
    #return Fine(**new_fine.__dict__)
    return {"message": "Fine created successfully"}

#agregar multas automaticamente
@router.post("/add_fine_automatically/")
def add_fine_automatically_route(db: Session = Depends(get_db)):
    """
    Endpoint para agregar multas automáticamente.
    Args:
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando que las multas se agregaron correctamente.
    """
    add_fine_automatically(db)
    return {"message": "Fines added successfully"}


#obtener fine por id_fine
@router.get("/fine/{id}", dependencies=[Depends(Portador())])
def get_fine(id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener los detalles de una multa por su ID.
    Args:
        id (int): ID de la multa.
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Detalles de la multa o un mensaje indicando que la multa no existe.
    """
    exist = exist_fine(id, db)
    if not exist:
        return {"message": "Fine not exist"}
    
    return FineCreate(**exist.__dict__)
    

#obtener todos los fines
@router.get("/all_finee/")
def get_all_fines(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todas las multas.
    Args:
        db (Session): Sesión de la base de datos.
    Returns:
        list: Lista de multas o un mensaje indicando que no hay multas.
    """
    return all_fines(db)

#pagar una multa
@router.put("/pay_fine/{id_fine}")
def pay_fine_route(id_fine: int, db: Session = Depends(get_db)):
    """
    Endpoint para pagar una multa.
    Args:
        id_fine (int): ID de la multa.
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando que la multa se pagó correctamente o que la multa no existe.
    """
    finePaid = pay_fine(id_fine, db)
    if not finePaid:
        return {"message": "Fine not exist"}
    return {"message": "Fine paid successfully"}

#perdonar una multa
@router.put("/forgive_fine/{id_fine}")
def forgive_fine_route(id_fine: int, db: Session = Depends(get_db)):
    """
    Endpoint para perdonar una multa.
    Args:
        id_fine (int): ID de la multa.
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando que la multa se perdonó correctamente o que la multa no existe.
    """
    fineForgiven = forgive_fine(id_fine, db)
    if not fineForgiven:
        return {"message": "Fine not exist"}
    return {"message": "Fine forgiven successfully"}

#eliminar fines por id_fine
@router.delete("/delete_fine/{id_fine}")
def delete_fine(id_fine: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar una multa por su ID.
    Args:
        id_fine (int): ID de la multa.
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando que la multa se eliminó correctamente o que la multa no existe.
    """
    fineDeleted = delete_fines(id_fine, db)
    if not fineDeleted:
        return {"message": "Fine not exist"}
    return {"message": "Fine deleted successfully"}

@router.delete("/delete_all_fines", dependencies=[Depends(Portador())])
def delete_all_fines_route(db: Session = Depends(get_db)):
    """
    Endpoint para eliminar todas las multas.
    Args:
        db (Session): Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando que todas las multas se eliminaron correctamente.
    """
    return delete_all_fines(db)