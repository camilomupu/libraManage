from datetime import date
from pydantic import BaseModel

class Report(BaseModel):
    fechaGeneracion: date
    numeroLibrosPrestados: int
    numeroLibrosNoDevueltos: int
    numeroComprasLibros: int
    id_usuario: int

class ReportOut(Report):
    id: int