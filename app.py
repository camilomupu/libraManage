from fastapi import FastAPI
from config.db import Base, engine
from routes import user, physicalBook, loan, digitalBook, buyBook, category, subcategory, author, fine

Base.metadata.create_all(bind=engine)
#Base.metadata.drop_all(engine) #borra toda la metadata, cuidado 

app = FastAPI()

app.include_router(user.router, tags=["User"])

app.include_router(physicalBook.router, tags=["PhysicalBook"])

app.include_router(loan.router, tags=["Loan"])

app.include_router(digitalBook.router, tags=["DigitalBook"])

app.include_router(buyBook.router, tags=["BuyBook"])

app.include_router(category.router, tags=["Category"])

app.include_router(subcategory.router, tags=["SubCategory"])  

app.include_router(author.router, tags=["Author"])  

app.include_router(fine.router, tags=["fine"])  

app.include_router(author.router, tags=["author"])  

@app.get("/", tags=["Main"])
def main():
    return {"message": "Hello World"}