from schemas.physicalBook import PhysicalBook
from schemas.user import UserCreate
from models.tables import LibroFisico, Multa, Prestamo, Usuario

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

def all_users(db):
    return db.query(Usuario).all()

def delete_users(id: int, db):
    usr = db.query(Usuario).filter(Usuario.id == id).first()
    db.delete(usr)
    db.commit()
    return usr

def exist_loan(id: int, db):#verificamos si el prestamo existe
    loan = db.query(Prestamo).filter(Prestamo.id == id).first()
    return loan

def get_associated_fine(id_user:int, id_prestamo: int, db):#obtenemos la multa asociada al prestamo
    multa = db.query(Multa).filter(Prestamo.id_usuario ==id_user , Multa.id_prestamo == id_prestamo).first()
    return multa

def exist_user_loan(id_user: int, db):#verificamos si el usuario tiene prestamos
    loan = db.query(Prestamo).filter(Prestamo.id_usuario == id_user).first()
    return loan


    
            
        

