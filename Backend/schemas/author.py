from pydantic import BaseModel

class Author(BaseModel):
    nombre: str
    
class AuthorOut(Author):
    id: int
