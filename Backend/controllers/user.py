from schemas.user import UserCreate
from models.tables import Usuario

def create_user(new_user: UserCreate, db):
    usr = Usuario(**new_user.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr

def exist_user(correo: str, db):
    usr = db.query(Usuario).filter(Usuario.correo == correo).first()
    return usr

def get_user(id: int, db):
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    return usr


def all_users(db):
    return db.query(Usuario).all()

def delete_users(id: int, db):
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    db.delete(usr)
    db.commit()
    return usr

