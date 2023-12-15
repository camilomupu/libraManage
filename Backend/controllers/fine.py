from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from schemas.fine import FineCreate, Fine
from models.tables import *
from sqlalchemy import func, text

def create_fine(new_fine: FineCreate, db):
    """
    Crea y registra una nueva multa en la base de datos.
    Args:
        new_fine (FineCreate): Datos de la nueva multa.
        db: Sesión de la base de datos.
    Returns:
        Multa: La multa creada y registrada en la base de datos.
    """
    fine = Multa(**new_fine.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(fine)
    db.commit()
    db.refresh(fine)
    return fine

def add_fine_automatically(db):
    """
    Añade multas automáticamente a los préstamos vencidos que no han sido devueltos.
    Args:
        db: Sesión de la base de datos.
    """
    four_days_ago = datetime.utcnow() - timedelta(days=4)
    overdue_loans = (
        db.query(Prestamo)
        .filter(Prestamo.fechaPrestamo < four_days_ago, Prestamo.devuelto != True)
        .all()
    )

    for loan in overdue_loans:
        existing_fine = db.query(Multa).filter(Multa.id_prestamo == loan.id).first()

        if not existing_fine:
            fecha_pago = (datetime.utcnow() + timedelta(days=15)).date()

            new_fine = Fine(
                valorDeuda=50000,
                estadoMulta=0,
                fechaDePago=fecha_pago,
                id_prestamo=loan.id
            )

            create_fine(new_fine, db)

def exist_fine(id_Fine: int, db):
    """
    Verifica la existencia de una multa en la base de datos.
    Args:
        id_Fine (int): ID de la multa a verificar.
        db: Sesión de la base de datos.
    Returns:
        Multa: La multa si existe, None si no existe.
    """
    fine = db.query(Multa).filter(Multa.id == id_Fine).first()
    return fine

def all_fines(db):
    """
    Obtiene todas las multas registradas en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        List[Multa]: Lista de todas las multas registradas.
    """
    return db.query(Multa).all()

def pay_fine(id_Fine: int, db):
    """
    Registra el pago de una multa en la base de datos.
    Args:
        id_Fine (int): ID de la multa a pagar.
        db: Sesión de la base de datos.
    Returns:
        Multa: La multa actualizada después de ser pagada.
    """
    fine = db.query(Multa).filter(Multa.id == id_Fine).first()
    fine.estadoMulta = 1 #NOTA PARA QUE NO SE NOS OLVIDE: 0 es pendiente, 1 es pagada y 2 es perdonada. 
    db.commit()
    db.refresh(fine)
    return fine

def forgive_fine(id_Fine: int, db):
    """
    Perdona una multa en la base de datos.
    Args:
        id_Fine (int): ID de la multa a perdonar.
        db: Sesión de la base de datos.
    Returns:
        Multa: La multa actualizada después de ser perdonada.
    """
    fine = db.query(Multa).filter(Multa.id == id_Fine).first()
    fine.estadoMulta = 2 #NOTA PARA QUE NO SE NOS OLVIDE: 0 es pendiente, 1 es pagada y 2 es perdonada. 
    db.commit()
    db.refresh(fine)
    return fine

def delete_fines(id_Fine: int, db):
    """
    Elimina una multa de la base de datos.
    Args:
        id_Fine (int): ID de la multa a eliminar.
        db: Sesión de la base de datos.
    Returns:
        Multa: La multa eliminada.
    """
    fine = db.query(Multa).filter(Multa.id == id_Fine).first()
    db.delete(fine)
    db.commit()
    max_id = db.query(func.max(Multa.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE multas_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return fine

def delete_all_fines(db):
    """
    Elimina todas las multas registradas en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        dict: Mensaje indicando el resultado de la operación.
    """
    try:
        db.query(Multa).delete()
        db.commit()
        return {"message": "All fines deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"message": f"An error occurred: {str(e)}"}