from datetime import date
from pydantic import BaseModel

class Fine(BaseModel):
    valorDeuda: int
    estadoMulta: str
    fechaDePago: str
    id_prestamo: int

class FineCreate(Fine):
    id: int