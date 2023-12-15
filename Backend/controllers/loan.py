from schemas.loan import Loan, LoanOut, loanDueDate
import datetime as dt
from models.tables import *
from sqlalchemy import func, text
from typing import List, Optional
from datetime import datetime

def create_loan(new_loan: Loan, db):
    loan = Prestamo(**new_loan.__dict__)
    fechaVencimiento = loan.fechaPrestamo + dt.timedelta(days=3)
    loan.fechaVencimiento = fechaVencimiento
    loan.devuelto = False
    db.add(loan)
    db.commit()
    db.refresh(loan)

    actualizar_informe_usuario(new_loan.id_usuario, db)

    return loan

def actualizar_informe_usuario(user_id: int, db):
    informe_usuario = db.query(Informe).filter(Informe.id_usuario == user_id).first()

    if informe_usuario:
        informe_usuario.numeroLibrosPrestados += 1

        db.commit()
        db.refresh(informe_usuario)
    else:

        nuevo_informe = Informe(
            fechaGeneracion=datetime.utcnow(),
            numeroLibrosPrestados=1,
            numeroLibrosNoDevueltos=0,
            numeroComprasLibros=0,
            id_usuario=user_id
        )

        db.add(nuevo_informe)
        db.commit()
        db.refresh(nuevo_informe)

def exist_loan(id_user: int, id_book: int, date_loan: Date, db):
    loan = db.query(Prestamo).filter((Prestamo.id_usuario == id_user) & (Prestamo.id_libroFisico == id_book) & 
                                      (Prestamo.fechaPrestamo == date_loan)).all()
    return loan


def check_availabilityWithDate(id_book: int, date: Date, db):
    # Calcular la fecha de vencimiento sumando 3 días a la fecha de préstamo
    fechaVencimiento = date + dt.timedelta(days=3)
    
    # Consultar préstamos que coinciden con el ID del libro y se superponen en fechas
    loan = db.query(Prestamo).filter((Prestamo.id_libroFisico == id_book) &(Prestamo.fechaVencimiento >= date) &
                                        (Prestamo.fechaPrestamo <= fechaVencimiento)).all()
    
    return loan

def check_availabilityToday(id_book: int,db):
    # Calcular la fecha de vencimiento sumando 3 días a la fecha de préstamo
    date = dt.date.today()
    fechaVencimiento = date + dt.timedelta(days=3)
    
    # Consultar préstamos que coinciden con el ID del libro y se superponen en fechas
    loan = db.query(Prestamo).filter((Prestamo.id_libroFisico == id_book) &(Prestamo.fechaVencimiento >= date) &
                                        (Prestamo.fechaPrestamo <= fechaVencimiento)).all()
    return loan

def all_loan(db):
    return db.query(Prestamo).all()

def all_loan_not_returned(db):
    return db.query(Prestamo).filter(Prestamo.devuelto == False).all()

def all_loan_by_user(id_user: int, db):
    return db.query(Prestamo).filter(Prestamo.id_usuario == id_user).all()

def return_loan_by_book_name_and_date(book_name: str, loan_date: dt.date, db):
    # Busca el libro físico por su nombre
    book = db.query(LibroFisico).filter_by(titulo=book_name).first()

    if book:
        # Busca el préstamo basado en el libro físico y la fecha de préstamo
        loan = db.query(Prestamo).filter(Prestamo.id_libroFisico == book.id,Prestamo.fechaPrestamo == loan_date).first()

        if loan:
            if not loan.devuelto:
                loan.devuelto = True
                db.commit()
                return loan
            else:
                return None  # El libro ya fue devuelto anteriormente
        else:
            return None  # Préstamo no encontrado
    else:
        return None  # Libro no encontrado

def return_loan_by_id(id_loan: int, db):
    # Busca el libro físico por su nombre
    loan = db.query(Prestamo).filter(Prestamo.id == id_loan).first()
    
    if loan:
        if not loan.devuelto:
            loan.devuelto = True
            db.commit()
            return loan
        else:
            return None  # El libro ya fue devuelto anteriormente
    else:
        return None  # Préstamo no encontrado

    
def delete_loan(id: int, db):
    loan = db.query(Prestamo).filter(Prestamo.id == id).first()
    db.delete(loan)
    db.commit()
    max_id = db.query(func.max(Prestamo.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE prestamos_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return loan

def delete_all_loans(db):
    try:
        db.query(Prestamo).delete()
        db.commit()
        return {"message": "All loans deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"message": f"An error occurred: {str(e)}"}
    
def get_loan(id: int, db):
    cat = db.query(Prestamo).filter(Prestamo.id == id).first()
    return cat


def update_loan(loan_id: int, updated_loan: Loan, db) -> Optional[Loan]:
        usr = get_loan(loan_id, db)
        if usr:
            usr.id_usuario = updated_loan.id_usuario
            usr.id_libroFisico = updated_loan.id_libroFisico
            usr.fechaPrestamo = updated_loan.fechaPrestamo
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None