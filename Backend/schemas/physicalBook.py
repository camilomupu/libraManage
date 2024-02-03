from pydantic import BaseModel
from fastapi import UploadFile, File


class PhysicalBook(BaseModel):
    titulo : str
    descripcion : str
    portada : str
    ubicacion : str
    estado : str
    id_autor : int
    id_subcategoria : int
    id_categoria : int

class PhysicalBookOut(PhysicalBook):    
    id: int