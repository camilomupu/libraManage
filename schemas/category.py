from pydantic import BaseModel

class Category(BaseModel):
    nombre: str
    descripcion: str
    
class CategoryOut(Category):
    id: int
