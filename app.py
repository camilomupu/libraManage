from fastapi import FastAPI
from config.db import Base, engine
from routes import user, rol, report

Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(engine) #borra toda la metadata, cuidado

app = FastAPI()
app.include_router(user.router, tags=["User"])
app.include_router(rol.router, tags=["Rol"])
app.include_router(report.router, tags=["Report"])


@app.get("/", tags=["Main"])
def main():
    return {"message": "Hello World"}
