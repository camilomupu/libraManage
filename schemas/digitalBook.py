from pydantic import BaseModel

class DigitalBookCreate(BaseModel):
    titulo: str
    descripcion: str
    link_libro: str
    #link_foto: str
    precio: float
    id_autor: int
    id_subcategoria: int
    id_categoria: int
    

class DBookOut(DigitalBookCreate):
    id: int
