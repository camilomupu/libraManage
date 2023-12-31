from fastapi import FastAPI
from config.db import Base, engine
from routes import user, physicalBook, loan

Base.metadata.create_all(bind=engine)
#Base.metadata.drop_all(engine) #borra toda la metadata, cuidado 

app = FastAPI()

app.include_router(user.router, tags=["User"])

app.include_router(physicalBook.router, tags=["PhysicalBook"])

app.include_router(loan.router, tags=["Loan"])


@app.get("/", tags=["Main"])
def main():
    return {"message": "Hello World"}