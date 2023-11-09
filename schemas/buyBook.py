from pydantic import BaseModel

class BuyBookCreate(BaseModel):
    id_usuario: int
    id_libroDigital: int
    

class BuyBookOut(BuyBookCreate):
    id: int
