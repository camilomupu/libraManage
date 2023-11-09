from datetime import date
from pydantic import BaseModel


class Fine(BaseModel):
    ValorDeuda: float
    EstadoFine: int
    fechaPago: date
    id_prestamo: int

class FineCreate(Fine):
    id_Fine: int