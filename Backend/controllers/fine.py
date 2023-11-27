from schemas.fine import FineCreate
from models.tables import *
from sqlalchemy import func, text

def create_fine(new_fine: FineCreate, db):

    fine = Multa(**new_fine.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(fine)
    db.commit()
    db.refresh(fine)
    return fine

def exist_fine(id_Fine: int, db):
    fine = db.query(Multa).filter(Multa.id_Fine == id_Fine).first()
    return fine

def all_fines(db):
    return db.query(Multa).all()

def delete_fines(id_Fine: int, db):
    fine = db.query(Multa).filter(Multa.id_Fine == id_Fine).first()
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