from datetime import date
from pydantic import BaseModel

class Loan(BaseModel):
    id: int
    fechaPrestamo : date    
    id_usuario : int
    id_libroFisico : int
    
class loanDueDate(Loan):
    fechaVencimiento : date

class LoanOut(loanDueDate):
    id : int
    
    
    