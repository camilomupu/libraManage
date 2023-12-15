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
    """
    Endpoint para crear un nuevo informe.
    Args:
        new_report (Report): Datos del informe.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Mensaje indicando que el informe se creó correctamente.
    """
    report = create_report(new_report, db)
    #return report
    return {"message": "Reporte created successfully"}

#obtener todos los informes
@router.get("/report/",response_model=list[Report])
def get_all_report(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los informes.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        list: Lista de informes o mensaje indicando que no hay informes.
    """
    return all_report(db)

#obtener informe por id
@router.get("/report/{id}", dependencies=[Depends(Portador())])
def get_report(id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un informe por su ID.
    Args:
        id (int): ID del informe.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Detalles del informe o mensaje indicando que no existe.
    """
    exist = exist_report(id, db)
    if not exist:
        return {"message": "Report not exist"}
    
    return ReportOut(**exist.__dict__)

#generar reporte
@router.get("/report/generate/", dependencies=[Depends(Portador())])
def generate_report_csv(db: Session = Depends(get_db)):
    """
    Endpoint para generar un informe en formato CSV.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Mensaje indicando que el informe se generó correctamente o que no hay datos.
    """
    return generate_report(db)

@router.get("/report/download-csv/", dependencies=[Depends(Portador())])
def generate_report_csv(db: Session = Depends(get_db)):
    """
    Endpoint para descargar un informe en formato CSV.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        Response: Archivo CSV descargable o mensajes de error.
    """
    report_data = generate_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    csv_content = generate_csv_content(report_data)

    if csv_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=csv_content.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=report.csv"})

@router.get("/report/download-csv-all-users/")
def generate_report_csv(db: Session = Depends(get_db)):
    """
    Endpoint para descargar un informe de todos los usuarios en formato CSV.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        Response: Archivo CSV descargable o mensajes de error.
    """
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
    """
    Endpoint para descargar un informe en formato XLSX.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        Response: Archivo XLSX descargable o mensajes de error.
    """
    report_data = generate_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    xlsx_content = generate_xlsx_content(report_data)

    if xlsx_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=xlsx_content.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=report.xlsx"})

#generar xlsx por usuario
@router.get("/report/download-xlsx-all-users/")
def generate_report_xlsx(db: Session = Depends(get_db)):
    """
    Endpoint para descargar un informe de todos los usuarios en formato XLSX.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        Response: Archivo XLSX descargable o mensajes de error.
    """
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
    """
    Endpoint para descargar un informe en formato PDF.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        Response: Archivo PDF descargable o mensajes de error.
    """
    report_data = generate_report(db)

    if report_data is None:
        return JSONResponse(status_code=404, content={"message": "No hay datos para generar el informe"})

    pdf_content = generate_pdf_content(report_data)

    if pdf_content is None:
        return JSONResponse(status_code=500, content={"message": "Error al generar el informe"})

    return Response(content=pdf_content.getvalue(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})

#generar pdf por usuario
@router.get("/report/download-pdf-all-users/")
def generate_report_pdf(db: Session = Depends(get_db)):
    """
    Endpoint para generar y descargar un informe en formato PDF para todos los usuarios.
    Args:
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        Response: Archivo PDF descargable o mensajes de error.
    """
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
    """
    Endpoint para eliminar un informe por su ID.
    Args:
        id (int): ID del informe.
        db (Session, optional): Sesión de la base de datos. Defaults to Depends(get_db).
    Returns:
        dict: Mensaje indicando que el informe se eliminó correctamente o que no existe.
    """
    reportDeleted = delete_report(id, db)
    if not reportDeleted:
        return {"message": "Report not exist"}
    return {"message": "Report deleted successfully", "user": Report(**reportDeleted.__dict__)}