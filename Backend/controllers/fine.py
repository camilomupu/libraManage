from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from schemas.fine import FineCreate, Fine
from models.tables import *
from sqlalchemy import func, text
from typing import List, Optional

def create_fine(new_fine: FineCreate, db):

    fine = Multa(**new_fine.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(fine)
    db.commit()
    db.refresh(fine)
    return fine

def add_fine_automatically(db):
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
    fine = db.query(Multa).filter(Multa.id == id_Fine).first()
    return fine

def all_fines(db):
    return db.query(Multa).all()

def pay_fine(id_Fine: int, db):
    fine = db.query(Multa).filter(Multa.id == id_Fine).first()
    fine.estadoMulta = 1 #NOTA PARA QUE NO SE NOS OLVIDE: 0 es pendiente, 1 es pagada y 2 es perdonada. 
    db.commit()
    db.refresh(fine)
    return fine

def forgive_fine(id_Fine: int, db):
    fine = db.query(Multa).filter(Multa.id == id_Fine).first()
    fine.estadoMulta = 2 #NOTA PARA QUE NO SE NOS OLVIDE: 0 es pendiente, 1 es pagada y 2 es perdonada. 
    db.commit()
    db.refresh(fine)
    return fine

def delete_fines(id_Fine: int, db):
    fine = db.query(Multa).filter(Multa.id == id_Fine).first()
    db.delete(fine)
    db.commit()
    max_id = db.query(func.max(Multa.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE multas_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return fine

def delete_all_fines(db):
    try:
        db.query(Multa).delete()
        db.commit()
        return {"message": "All fines deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"message": f"An error occurred: {str(e)}"}
    

def get_fine(id: int, db):
    cat = db.query(Multa).filter(Multa.id == id).first()
    return cat


def update_fine(fine_id: int, updated_fine: Fine, db) -> Optional[Fine]:
        usr = get_fine(fine_id, db)
        if usr:
            usr.valorDeuda = updated_fine.valorDeuda
            usr.estadoMulta = updated_fine.estadoMulta
            usr.fechaDePago = updated_fine.fechaDePago
            usr.id_prestamo = updated_fine.id_prestamo
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None
