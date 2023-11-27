from datetime import date
from pydantic import BaseModel


class Loan(BaseModel):
    id: int
    fechaPrestamo : date    
    fechaVemcimiento : date
    id_usuario : int
    id_libroFisico : int

class LoanOut(Loan):
    id : int
    
    