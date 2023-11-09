from pydantic import BaseModel

class PhysicalBook(BaseModel):
    titulo : str
    descripcion : str
    ubicacion : str
    id_autor : int
    id_subcategoria : int
    id_categoria : int