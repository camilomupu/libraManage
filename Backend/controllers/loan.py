from schemas.loan import Loan, LoanOut, loanDueDate
import datetime as dt
from models.tables import *
from sqlalchemy import func, text

def create_loan(new_loan: Loan, db):
    """
    Crea un nuevo préstamo en la base de datos.
    Args:
        new_loan (Loan): Objeto que contiene los detalles del préstamo.
        db: Sesión de la base de datos.
    Returns:
        Prestamo: Objeto del préstamo creado.
    """
    loan = Prestamo(**new_loan.__dict__)
    fechaVencimiento = loan.fechaPrestamo + dt.timedelta(days=3)
    loan.fechaVencimiento = fechaVencimiento
    loan.devuelto = False
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def exist_loan(id_user: int, id_book: int, date_loan: Date, db):
    """
    Verifica si existe un préstamo dado el ID de usuario, ID de libro y fecha de préstamo.
    Args:
        id_user (int): ID de usuario.
        id_book (int): ID de libro físico.
        date_loan (Date): Fecha de préstamo.
        db: Sesión de la base de datos.
    Returns:
        List[Prestamo]: Lista de préstamos que cumplen con los criterios de búsqueda.
    """
    loan = db.query(Prestamo).filter((Prestamo.id_usuario == id_user) & (Prestamo.id_libroFisico == id_book) & 
                                      (Prestamo.fechaPrestamo == date_loan)).all()
    return loan


def check_availabilityWithDate(id_book: int, date: Date, db):
    """
    Verifica la disponibilidad de un libro físico para préstamo en una fecha específica.
    Args:
        id_book (int): ID del libro físico.
        date (Date): Fecha de préstamo.
        db: Sesión de la base de datos.
    Returns:
        List[Prestamo]: Lista de préstamos que coinciden en fechas con la solicitud.
    """
    # Calcular la fecha de vencimiento sumando 3 días a la fecha de préstamo
    fechaVencimiento = date + dt.timedelta(days=3)
    
    # Consultar préstamos que coinciden con el ID del libro y se superponen en fechas
    loan = db.query(Prestamo).filter((Prestamo.id_libroFisico == id_book) &(Prestamo.fechaVencimiento >= date) &
                                        (Prestamo.fechaPrestamo <= fechaVencimiento)).all()
    
    return loan

def check_availabilityToday(id_book: int,db):
    """
    Verifica la disponibilidad de un libro físico para préstamo en la fecha actual.
    Args:
        id_book (int): ID del libro físico.
        db: Sesión de la base de datos.
    Returns:
        List[Prestamo]: Lista de préstamos que coinciden en fechas con la solicitud actual.
    """
    # Calcular la fecha de vencimiento sumando 3 días a la fecha de préstamo
    date = dt.date.today()
    fechaVencimiento = date + dt.timedelta(days=3)
    
    # Consultar préstamos que coinciden con el ID del libro y se superponen en fechas
    loan = db.query(Prestamo).filter((Prestamo.id_libroFisico == id_book) &(Prestamo.fechaVencimiento >= date) &
                                        (Prestamo.fechaPrestamo <= fechaVencimiento)).all()
    return loan

def all_loan(db):
    """
    Obtiene todos los préstamos registrados en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        List[Prestamo]: Lista de todos los préstamos.
    """
    return db.query(Prestamo).all()

def return_loan_by_book_name_and_date(book_name: str, loan_date: dt.date, db):
    """
    Devuelve un préstamo dado el nombre del libro y la fecha de préstamo.
    Args:
        book_name (str): Nombre del libro físico.
        loan_date (dt.date): Fecha de préstamo.
        db: Sesión de la base de datos.
    Returns:
        Prestamo or None: Objeto de préstamo si existe, None si no se encuentra.
    """
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
    """
    Marca como devuelto un préstamo basado en su ID.
    Args:
        id_loan (int): ID del préstamo.
        db: Sesión de la base de datos.
    Returns:
        Prestamo or None: Objeto del préstamo si existe y no ha sido devuelto, None si no se encuentra o ya fue devuelto.
    """
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
    """
    Elimina un préstamo de la base de datos basado en su ID.
    Args:
        id (int): ID del préstamo.
        db: Sesión de la base de datos.
    Returns:
        Prestamo or None: Objeto del préstamo eliminado si existe, None si no se encuentra.
    """
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