from pydantic import BaseModel

class BuyBookCreate(BaseModel):
    id_usuario: int
    id_libroDigital: int
    

class BuyBookCreateNameBook(BaseModel):
    id_usuario: int
    name_ibroDigital: str
    

class BuyBookOut(BuyBookCreate):
    id: int
