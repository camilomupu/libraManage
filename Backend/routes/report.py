#van a ir todas las rutas relacionadas con el informe
import io
from fastapi import APIRouter, Depends, Response
from http.client import HTTPException
from fastapi.responses import JSONResponse
from schemas.report import Report, ReportOut
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.report import create_report, exist_report, all_report, delete_report, generate_report, generate_csv_content, generate_xlsx_content, generate_pdf_content, generate_csv_content_by_user, generate_xlsx_content_by_user, generate_pdf_content_by_user
from routes.user import Portador


router = APIRouter()

#crear informe
@router.post("/reportcreate/", dependencies=[Depends(Portador())])
def create_new_report(new_report: Report, db: Session = Depends(get_db)):
    report = create_report(new_report, db)
    return report

#obtener todos los informes
@router.get("/report/",response_model=list[Report], dependencies=[Depends(Portador())])
def get_all_report(db: Session = Depends(get_db)):
    return all_report(db)

#obtener informe por id
@router.get("/report/{id}", dependencies=[Depends(Portador())])
def get_report(id: int, db: Session = Depends(get_db)):
    exist = exist_report(id, db)
    if not exist:
        return {"message": "Report not exist"}
    
    return ReportOut(**exist.__dict__)

#generar reporte
@router.get("/report/generate/", dependencies=[Depends(Portador())])
def generate_report_csv(db: Session = Depends(get_db)):
    return generate_report(db)

@router.get("/report/download-csv/", dependencies=[Depends(Portador())])
def generate_report_csv(db: Session = Depends(get_db)):
    report_data = generate_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    csv_content = generate_csv_content(report_data)

    if csv_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=csv_content.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=report.csv"})

@router.get("/report/download-csv-all-users/", dependencies=[Depends(Portador())])
def generate_report_csv(db: Session = Depends(get_db)):
    report_data = all_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    csv_content = generate_csv_content_by_user(report_data, db)

    if csv_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=csv_content.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=report_users.csv"})

#generar xlsx
@router.get("/report/download-xlsx/", dependencies=[Depends(Portador())])
def generate_report_xlsx(db: Session = Depends(get_db)):
    report_data = generate_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    xlsx_content = generate_xlsx_content(report_data)

    if xlsx_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=xlsx_content.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=report.xlsx"})

#generar xlsx por usuario
@router.get("/report/download-xlsx-all-users/", dependencies=[Depends(Portador())])
def generate_report_xlsx(db: Session = Depends(get_db)):
    report_data = all_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    xlsx_content = generate_xlsx_content_by_user(report_data, db)

    if xlsx_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=xlsx_content.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=report_users.xlsx"})

#generar pdf
@router.get("/report/download-pdf/", dependencies=[Depends(Portador())])
def generate_report_pdf(db: Session = Depends(get_db)):
    report_data = generate_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    pdf_content = generate_pdf_content(report_data)

    if pdf_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=pdf_content.getvalue(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})

#generar pdf por usuario
@router.get("/report/download-pdf-all-users/", dependencies=[Depends(Portador())])
def generate_report_pdf(db: Session = Depends(get_db)):
    report_data = all_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    pdf_content = generate_pdf_content_by_user(report_data, db)

    if pdf_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=pdf_content.getvalue(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report_users.pdf"})

#eliminar informe por id
@router.delete("/report/delete/{id}", dependencies=[Depends(Portador())])
def del_report(id: int, db: Session = Depends(get_db)):
    reportDeleted = delete_report(id, db)
    if not reportDeleted:
        return {"message": "Report not exist"}
    return {"message": "Report deleted successfully", "user": Report(**reportDeleted.__dict__)}