from pydantic import BaseModel
from fastapi import UploadFile, File


class PhysicalBook(BaseModel):
    titulo : str
    descripcion : str
    ubicacion : str
    #imagen : UploadFile = File(None)
    id_autor : int
    id_subcategoria : int
    id_categoria : int

class PhysicalBookOut(PhysicalBook):    
    id: int