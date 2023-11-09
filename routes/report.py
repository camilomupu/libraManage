#van a ir todas las rutas relacionadas con el informe
from fastapi import APIRouter, Depends
from schemas.report import Report
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.report import create_report, exist_report, all_report, delete_report

router = APIRouter()

#crear informe
@router.post("/reportcreate/")
def create_new_report(new_report: Report, db: Session = Depends(get_db)):
    report = create_report(new_report, db)
    return report

#obtener todos los informes
@router.get("/report/",response_model=list[Report])
def get_all_report(db: Session = Depends(get_db)):
    return all_report(db)

#obtener informe por id
@router.get("/report/{id}")
def get_report(id: str, db: Session = Depends(get_db)):
    exist = exist_report(id, db)
    if not exist:
        return {"message": "Report not exist"}
    
    return Report(**exist.__dict__)

#eliminar informe por id
@router.delete("/report/delete/{id}")
def del_report(id: str, db: Session = Depends(get_db)):
    reportDeleted = delete_report(id, db)
    if not reportDeleted:
        return {"message": "Report not exist"}
    return {"message": "Report deleted successfully", "user": Report(**reportDeleted.__dict__)}