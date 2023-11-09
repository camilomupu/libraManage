from fastapi import APIRouter, Depends
from schemas.loan import Loan
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.loan import create_loan, exist_loan, all_loan, delete_loan

router = APIRouter()

#nuevo prestamo
@router.post("/new_loan/")
def create_new_loan(loan: Loan, db: Session = Depends(get_db)):
    exist = exist_loan(loan.id, db)
    if exist:
        return {"message": "Loan already exist"}
    new_loan = create_loan(loan,db)
    return Loan(**new_loan.__dict__)

#obtener prestamo por id  
@router.get("/loan/{id}")
def get_loan(id: str, db: Session = Depends(get_db)):
    exist = exist_loan(id, db)
    if not exist:
        return {"message": "Loan not exist"}
    
    return Loan(**exist.__dict__)

#obtener todos los prestamos
@router.get("/all_loans/", response_model=list[Loan])
def get_all_loan(db: Session = Depends(get_db)):
    return all_loan(db)

#eliminar prestamo por id
@router.delete("/delete_loan/{id}")
def delete_loan_id(id:str, db:Session = Depends(get_db)):
    loanDeleted = delete_loan(id, db)
    if not loanDeleted:
        return {"message": "Loan not exist"}
    return {"message": "Loan deleted successfully", "loan": Loan(**loanDeleted.__dict__)}