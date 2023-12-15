from pydantic import BaseModel

class DigitalBookCreate(BaseModel):
    titulo: str
    portada : str
    descripcion: str
    link_Libro: str
    precio: float
    id_autor: int
    id_subcategoria: int
    id_categoria: int
    

class DBookOut(DigitalBookCreate):
    id: int
