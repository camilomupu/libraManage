from datetime import date
from pydantic import BaseModel

class Loan(BaseModel):
    fechaPrestamo : date    
    id_usuario : int
    id_libroFisico : int
    
class loanDueDate(Loan):
    fechaVemcimiento : date

class LoanOut(loanDueDate):
    id : int
    
    
    