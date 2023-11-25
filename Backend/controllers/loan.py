from schemas.loan import Loan, LoanOut, loanDueDate
import datetime as dt
from models.tables import *

def create_loan(new_loan: Loan, db):
    loan = Prestamo(**new_loan.__dict__)
    fechaVemcimiento = loan.fechaPrestamo + dt.timedelta(days=3)
    loan.fechaVemcimiento = fechaVemcimiento
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def exist_loan(id_user: int, id_book: int, date_loan: Date, db):
    loan = db.query(Prestamo).filter((Prestamo.id_usuario == id_user) & (Prestamo.id_libroFisico == id_book) & 
                                      (Prestamo.fechaPrestamo == date_loan)).all()
    return loan


def check_availabilityWithDate(id_book: int, date: Date, db):
    # Calcular la fecha de vencimiento sumando 3 días a la fecha de préstamo
    fechaVencimiento = date + dt.timedelta(days=3)
    
    # Consultar préstamos que coinciden con el ID del libro y se superponen en fechas
    loan = db.query(Prestamo).filter((Prestamo.id_libroFisico == id_book) &(Prestamo.fechaVemcimiento >= date) &
                                        (Prestamo.fechaPrestamo <= fechaVencimiento)).all()
    
    return loan

def check_availabilityToday(id_book: int,db):
    # Calcular la fecha de vencimiento sumando 3 días a la fecha de préstamo
    date = dt.date.today()
    fechaVencimiento = date + dt.timedelta(days=3)
    
    # Consultar préstamos que coinciden con el ID del libro y se superponen en fechas
    loan = db.query(Prestamo).filter((Prestamo.id_libroFisico == id_book) &(Prestamo.fechaVemcimiento >= date) &
                                        (Prestamo.fechaPrestamo <= fechaVencimiento)).all()
    return loan

def all_loan(db):
    return db.query(Prestamo).all()

def delete_loan(id: int, db):
    loan = db.query(Prestamo).filter(Prestamo.id == id).first()
    db.delete(loan)
    db.commit()
    return loan