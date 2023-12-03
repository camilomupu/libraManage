from pydantic import BaseModel

class Author(BaseModel):
    id : int
    nombre: str
    
class AuthorOut(Author):
    id: int
