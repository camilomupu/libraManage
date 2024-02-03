from schemas.buyBook import BuyBookCreate, BuyBookCreateNameBook, BuyBookOut
from models.tables import *
from sqlalchemy import func, text
from typing import List, Optional
from datetime import datetime

def create_BuyDBooks(nuevo_BuyDBook: BuyBookCreate, db):
    """
    Crea un nuevo registro de CompraLibro en la base de datos.
    Args:
        nuevo_BuyDBook (BuyBookCreate): Objeto que contiene la información del libro a comprar.
        db: Sesión de la base de datos.
    Returns:
        CompraLibro: El objeto CompraLibro recién creado.
    """
    compLibro = CompraLibro(**nuevo_BuyDBook.dict())
    db.add(compLibro)
    db.commit()
    db.refresh(compLibro)
    return compLibro

def create_BuyDBooks(nuevo_BuyDBook: BuyBookCreateNameBook, db):
    compLibro = CompraLibro(**nuevo_BuyDBook.dict())
    db.add(compLibro)
    db.commit()
    db.refresh(compLibro)

    actualizar_informe_usuario(nuevo_BuyDBook.id_usuario, db)

    return compLibro

def actualizar_informe_usuario(user_id: int, db):
    informe_usuario = db.query(Informe).filter(Informe.id_usuario == user_id).first()

    if informe_usuario:

        informe_usuario.numeroComprasLibros += 1 

        db.commit()
        db.refresh(informe_usuario)
    else:

        nuevo_informe = Informe(
            fechaGeneracion=datetime.utcnow(),
            numeroLibrosPrestados=0,
            numeroLibrosNoDevueltos=0, 
            numeroComprasLibros=1,
            id_usuario=user_id
        )

        db.add(nuevo_informe)
        db.commit()
        db.refresh(nuevo_informe)


def exist_BuyDBook(id_user: int, id_dBook: int, db):
    """
    Verifica si existe una compra de libro para un usuario y un libro digital específicos.
    Args:
        id_user (int): ID del usuario.
        id_dBook (int): ID del libro digital.
        db: Sesión de la base de datos.
    Returns:
        CompraLibro or None: El objeto CompraLibro si existe, None si no se encuentra.
    """
    compLibros = db.query(CompraLibro).filter((CompraLibro.id_usuario == id_user) & (CompraLibro.id_libroDigital == id_dBook)).first()
    return compLibros

def get_BuysDBooks(id_user: int, db):
    """
    Obtiene todas las compras de libros digitales asociadas a un usuario.
    Args:
        id_user (int): ID del usuario.
        db: Sesión de la base de datos.
    Returns:
        sqlalchemy.orm.Query: Consulta que representa las compras de libros digitales asociadas al usuario.
    """
    compLibros = db.query(CompraLibro).filter(CompraLibro.id_usuario == id_user )
    return compLibros

def all_BuyDBooks(db):
    """
    Obtiene todos los registros de compras de libros digitales en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        List[CompraLibro]: Lista que contiene todos los registros de CompraLibro.
    """
    return db.query(CompraLibro).all()

def all_BuyDBooks_by_user(id_user: int, db):
    return db.query(CompraLibro).filter(CompraLibro.id_usuario == id_user).all()

def delete_BuyDBook(id: int, db):
    """
    Elimina un registro de compra de libro digital por su ID.
    Args:
        id (int): ID de la compra de libro digital a eliminar.
        db: Sesión de la base de datos.
    Returns:
        CompraLibro or dict: El objeto CompraLibro eliminado o un diccionario con un mensaje de error.
    """
    try:
        compLibro = db.query(CompraLibro).filter(CompraLibro.id == id).first()
        if compLibro:
            db.delete(compLibro)
            db.commit()

            # Obtener el valor máximo actual del id
            max_id = db.query(func.max(CompraLibro.id)).scalar()

            # Reiniciar la secuencia con el siguiente valor
            db.execute(text(f"ALTER SEQUENCE compraLibros_id_seq RESTART WITH {max_id + 1}"))

            return compLibro
        else:
            return {"message": "CompraLibro not found"}
    except Exception as e:
        db.rollback()
        return {"message": f"An error occurred: {str(e)}"}
    
    
    
    """compLibro = db.query(CompraLibro).filter(CompraLibro.id == id).first()
    db.delete(compLibro)
    db.commit()
    max_id = db.query(func.max(CompraLibro.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE comprasLibros_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return compLibro"""

def delete_all_buy_books(db):
    """
    Elimina todos los registros de compras de libros digitales en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        dict: Un diccionario con un mensaje indicando el resultado de la operación.
    """
    try:
        db.query(CompraLibro).delete()
        db.commit()
        return {"message": "All BuyBook records deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"message": f"An error occurred: {str(e)}"}
    
def get_buybookcreate(id: int, db):
    cat = db.query(CompraLibro).filter(CompraLibro.id == id).first()
    return cat


def update_buybookcreate(buybookcreate_id: int, updated_buybookcreate: BuyBookCreate, db) -> Optional[BuyBookCreate]:
        usr = get_buybookcreate(buybookcreate_id, db)
        if usr:
            usr.id_usuario = updated_buybookcreate.id_usuario
            usr.id_libroDigital = updated_buybookcreate.id_libroDigital
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None

