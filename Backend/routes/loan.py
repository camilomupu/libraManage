from fastapi import APIRouter, Depends
from schemas.loan import Loan, LoanOut, loanDueDate
from config.db import get_db
from sqlalchemy.orm import Session
import datetime as dt
from controllers.loan import create_loan, exist_loan, all_loan, delete_loan, check_availabilityWithDate,check_availabilityToday,delete_all_loans, return_loan_by_book_name_and_date,return_loan_by_id
from controllers.physicalBook import get_physicalBook
from controllers.user import get_user
from controllers.email import *


router = APIRouter()

#nuevo prestamo
@router.post("/new_loan/")
async def create_new_loan(loan: Loan, db: Session = Depends(get_db)):
    exist = exist_loan(loan.id_usuario, loan.id_libroFisico, loan.fechaPrestamo, db)
    if exist:
        return {"message": "This loan is already registered"}
    exist = check_availabilityWithDate(loan.id_libroFisico, loan.fechaPrestamo, db)
    if exist:
        return {"message": "This book is not available for this date"}
    bookExist = get_physicalBook(loan.id_libroFisico, db)
    if not bookExist:
        return {"message": "the physical book does not exist"}
    userExist = get_user(loan.id_usuario, db)
    if not userExist:
        return {"message": "the user does not exist"}
    new_loan = create_loan(loan,db)
    await sendEmaiLoanConfirmation(userExist.correo, bookExist, new_loan, userExist)
    #return loanDueDate(**new_loan.__dict__)
    return {"message": "Loan created successfully"}

#obtener prestamo por id  
@router.get("/loan/{id_user}/{id_book}/{date}")
def get_loan(id_user: int, id_book: int, date_loan: dt.date, db: Session = Depends(get_db)):
    exist = exist_loan(id_user, id_book, date_loan, db)
    if not exist:
        return {"message": "Loan not exist"}
    return exist

@router.get("/check_availability/{id_book}/{date}")
def get_loan(id_book: int, date: dt.date, db: Session = Depends(get_db)):
    exist = check_availabilityWithDate(id_book, date, db)
    if not exist:
        return {"message": "Loan not exist"}
    return exist

#obtener todos los prestamos
@router.get("/all_loans/", response_model=list[LoanOut])
def get_all_loan(db: Session = Depends(get_db)):
    return all_loan(db)

@router.put("/return_loan_by_book_name_and_date/")
def return_loan_by_book_name_and_date_endpoint(book_name: str, loan_date: dt.date, db: Session = Depends(get_db)):
    returned_loan = return_loan_by_book_name_and_date(book_name, loan_date, db)
    if returned_loan:
        return returned_loan
    else:
        return {"message": "Loan not found"}
    
@router.put("/return_loan_by_id/")
def return_loan_by_id_endpoint(id_loan:int, db: Session = Depends(get_db)):
    returned_loan = return_loan_by_id(id_loan, db)
    if returned_loan:
        return returned_loan
    else:
        return {"message": "Loan not found"}

#eliminar prestamo por id
@router.delete("/delete_loan/{id}")
def delete_loan_id(id:int, db:Session = Depends(get_db)):
    loanDeleted = delete_loan(id, db)
    if not loanDeleted:
        return {"message": "Loan not exist"}
    return {"message": "Loan deleted successfully", "loan": Loan(**loanDeleted.__dict__)}

@router.delete("/delete_all_loans")
def delete_all_loans_route(db: Session = Depends(get_db)):
    return delete_all_loans(db)