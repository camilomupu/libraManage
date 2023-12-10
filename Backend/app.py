from fastapi import FastAPI, File, UploadFile
from config.db import Base, engine
from routes import user, physicalBook, loan, digitalBook, buyBook, category, subcategory, author, fine, rol, report, book
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
#Base.metadata.drop_all(engine) #borra toda la metadata, cuidado
#colocar nombre
app = FastAPI(title="Libra Tech", description="API para el manejo de una biblioteca", version="1.0.0")

origins = [
    
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(user.router, tags=["User"])

app.include_router(physicalBook.router, tags=["PhysicalBook"])

app.include_router(loan.router, tags=["Loan"])

app.include_router(digitalBook.router, tags=["DigitalBook"])

app.include_router(buyBook.router, tags=["BuyBook"])

app.include_router(category.router, tags=["Category"])

app.include_router(subcategory.router, tags=["SubCategory"])  

app.include_router(author.router, tags=["Author"])  

app.include_router(fine.router, tags=["Fine"])  

app.include_router(rol.router, tags=["Rol"])

app.include_router(report.router, tags=["Report"])

app.include_router(book.router, tags=["Book"])


@app.get("/", tags=["Main"])
def main():
    return {"message": "Hello World"}
