from schemas.buyBook import BuyBookCreate, BuyBookCreateNameBook, BuyBookOut
from models.tables import *
from sqlalchemy import func, text

def create_BuyDBooks(nuevo_BuyDBook: BuyBookCreate, db):
    compLibro = CompraLibro(**nuevo_BuyDBook.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(compLibro)
    db.commit()
    db.refresh(compLibro)
    return compLibro

def create_BuyDBooks(nuevo_BuyDBook: BuyBookCreateNameBook, db):
    compLibro = CompraLibro(**nuevo_BuyDBook.dict())
    ## Acá va la logica de consulta en la base de datos
    db.add(compLibro)
    db.commit()
    db.refresh(compLibro)
    return compLibro

def exist_BuyDBook(id_user: int, id_dBook: int, db):
    compLibros = db.query(CompraLibro).filter((CompraLibro.id_usuario == id_user) & (CompraLibro.id_libroDigital == id_dBook)).first()
    return compLibros

def get_BuysDBooks(id_user: int, db):
    compLibros = db.query(CompraLibro).filter(CompraLibro.id_usuario == id_user )
    return compLibros

def all_BuyDBooks(db):
    return db.query(CompraLibro).all()

def delete_BuyDBook(id: int, db):
    compLibro = db.query(CompraLibro).filter(CompraLibro.id == id).first()
    db.delete(compLibro)
    db.commit()
    max_id = db.query(func.max(CompraLibro.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE comprasLibros_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return compLibro

def delete_all_buy_books(db):
    try:
        db.query(CompraLibro).delete()
        db.commit()
        return {"message": "All BuyBook records deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"message": f"An error occurred: {str(e)}"}

