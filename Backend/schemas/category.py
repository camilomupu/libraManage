from pydantic import BaseModel

class Category(BaseModel):
    nombre: str
    
class CategoryOut(Category):
    id: int
