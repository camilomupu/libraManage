from pydantic import BaseModel

class SubCategory(BaseModel):
    nombre: str

class SubCategoryOut(SubCategory):
    id: int