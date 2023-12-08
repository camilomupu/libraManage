#van a ir todas las rutas relacionadas con el buyBook
from fastapi import APIRouter, Depends, Request
from schemas.buyBook import BuyBookCreate, BuyBookOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.buyBook import create_BuyDBooks, exist_BuyDBook, all_BuyDBooks, delete_BuyDBook, get_BuysDBooks, delete_all_buy_books
from controllers.digitalBook import get_dBook
from controllers.user import get_user
from fastapi.responses import HTMLResponse
from controllers.email import *
from routes.user import Portador

router = APIRouter()

#nuevo buyBook pruebas
@router.post("/new_buyBook/", dependencies=[Depends(Portador())])
async def create_new_buy_digital_book(buyBook: BuyBookCreate, db: Session = Depends(get_db)):
    buyExist = exist_BuyDBook(buyBook.id_usuario, buyBook.id_libroDigital, db)
    if buyExist:
       return {"message": "Buy digital book already exist"}
    bookExist = get_dBook(buyBook.id_libroDigital, db)
    if not bookExist:
        return {"message": "the digital book does not exist"}
    userExist = get_user(buyBook.id_usuario, db)
    if not userExist:
        return {"message": "the user does not exist"}
    new_user = create_BuyDBooks(buyBook,db)
    await sendEmailSaleConfirmation(userExist.correo, bookExist, userExist)
    #return BuyBookCreate(**new_user.__dict__)
    return {"message": "Buy digital book created successfully"}


#obtener compra por id del usuario y id del libro digital
@router.get("/buyBook/{id_user}/{id_dBook}", dependencies=[Depends(Portador())])
def get_buy_digital_book(id_user: int ,id_dBook: int, db: Session = Depends(get_db)):
    exist = exist_BuyDBook(id_user, id_dBook, db)
    if not exist:
        return {"message": "Buy digital book not exist"}
    
    return BuyBookOut(**exist.__dict__)

#obtener todos los buyBooks
@router.get("/all_buyBooks/", response_model=list[BuyBookCreate])
def get_all_buy_digital_books(db: Session = Depends(get_db)):
    return all_BuyDBooks(db)

#eliminar buyBooks por id
@router.delete("/delete_buyBook/{id}", dependencies=[Depends(Portador())])
def delete_buy_digital_book(id: int, db: Session = Depends(get_db)):
    buyBookDeleted = delete_BuyDBook(id, db)
    if not buyBookDeleted:
        return {"message": "Buy digital book not exist"}
    return {"message": "Buy digital book deleted successfully"}

@router.delete("/delete_all_buy_books", dependencies=[Depends(Portador())])
def delete_all_buy_books_route(db: Session = Depends(get_db)):
    return delete_all_buy_books(db)