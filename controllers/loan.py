from schemas.loan import Loan
from models.tables import *

def create_loan(new_loan: Loan, db):
    loan = Prestamo(**new_loan.__dict__)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def exist_loan(id:int, db):
    loan = db.query(Prestamo).filter(Prestamo.id == id).first()
    return loan

def all_loan(db):
    return db.query(Prestamo).all()

def delete_loan(id: int, db):
    loan = db.query(Prestamo).filter(Prestamo.id == id).first()
    db.delete(loan)
    db.commit()
    return loan