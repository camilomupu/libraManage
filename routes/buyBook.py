#van a ir todas las rutas relacionadas con el buyBook
from fastapi import APIRouter, Depends
from schemas.buyBook import BuyBookCreate, BuyBookOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.buyBook import create_BuyDBooks, exist_BuyDBook, all_BuyDBooks, delete_BuyDBook


router = APIRouter()

#nuevo buyBook
@router.post("/new_buyBook/")
def create_new_buy_digital_book(buyBook: BuyBookCreate, db: Session = Depends(get_db)):
    exist = exist_BuyDBook(buyBook.id_usuario, buyBook.id_libroDigital, db)
    if exist:
        return {"message": "Buy digital book already exist"}
    new_user = create_BuyDBooks(buyBook,db)
    return BuyBookCreate(**new_user.__dict__)


#obtener buyBook por correo
@router.get("/buyBook/{id_user}/{id_dBook}")
def get_buy_digital_book(id_user: int ,id_dBook: int, db: Session = Depends(get_db)):
    exist = exist_BuyDBook(id_user, id_dBook, db)
    if not exist:
        return {"message": "Buy digital book not exist"}
    
    return BuyBookCreate(**exist.__dict__)
    

#obtener todos los buyBooks
@router.get("/all_buyBooks/", response_model=list[BuyBookOut])
def get_all_buy_digital_books(db: Session = Depends(get_db)):
    return all_BuyDBooks(db)

#eliminar buyBooks por id
@router.delete("/delete_buyBook/{id}")
def delete_buy_digital_book(id: int, db: Session = Depends(get_db)):
    buyBookDeleted = delete_BuyDBook(id, db)
    if not buyBookDeleted:
        return {"message": "Buy digital book not exist"}
    return {"message": "Buy digital book deleted successfully", "Buy digital book": BuyBookCreate(**buyBookDeleted.__dict__)}