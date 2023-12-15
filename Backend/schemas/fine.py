from datetime import date
from pydantic import BaseModel

class Fine(BaseModel):
    valorDeuda: int
    estadoMulta: int
    fechaDePago: date
    id_prestamo: int

class FineCreate(Fine):
    id: int