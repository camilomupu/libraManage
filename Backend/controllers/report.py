import csv
import openpyxl
import datetime as dt
from io import StringIO, BytesIO
from schemas.report import Report
from models.tables import Informe, Usuario
from sqlalchemy import func, text
from reportlab.pdfgen import canvas
from typing import List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_report(new_report: Report, db):
    """
    Crea un nuevo informe en la base de datos.
    Args:
        new_report (Report): Objeto que contiene la información del nuevo informe.
        db: Sesión de la base de datos.
    Returns:
        Report: Objeto del informe creado.
    """
    report = Informe(**new_report.dict())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def exist_report(id: int, db):
    """
    Verifica la existencia de un informe en la base de datos por su ID.
    Args:
        id (int): ID del informe.
        db: Sesión de la base de datos.
    Returns:
        Report or None: Objeto del informe si existe, None si no se encuentra.
    """
    report = db.query(Informe).filter(Informe.id == id).first()
    return report

def all_report(db):
    """
    Obtiene todos los informes de la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        list: Lista de objetos de informes.
    """
    return db.query(Informe).all()

def delete_report(id: int, db):
    """
    Elimina un informe de la base de datos por su ID.
    Args:
        id (int): ID del informe.
        db: Sesión de la base de datos.
    Returns:
        Report or None: Objeto del informe eliminado si existe, None si no se encuentra.
    """
    delReport = db.query(Informe).filter(Informe.id == id).first()
    db.delete(delReport)
    db.commit()
    max_id = db.query(func.max(Informe.id)).scalar()
    db.execute(text(f"ALTER SEQUENCE informes_id_seq RESTART WITH {max_id + 1}"))
    print(max_id)
    db.commit()
    return delReport

def generate_report(db):
    """
    Genera un informe general a partir de los datos almacenados en la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        dict: Diccionario con la información del informe general.
    """
    fecha_generacion = dt.datetime.now()
    fecha_formateada = fecha_generacion.strftime("%Y-%m-%d %H:%M:%S")

    suma_resultados = (
            db.query(
                func.sum(Informe.numeroLibrosPrestados).label("total_libros_prestados"),
                func.sum(Informe.numeroComprasLibros).label("total_compras_libros"),
                func.sum(Informe.numeroLibrosNoDevueltos).label("total_libros_no_devueltos")
            )
        ).first()
    
    if suma_resultados:
        total_libros_prestados = suma_resultados.total_libros_prestados
        total_libros_comprados = suma_resultados.total_compras_libros
        total_libros_no_devueltos = suma_resultados.total_libros_no_devueltos
    else:
        total_libros_prestados = 0
        total_libros_comprados = 0
        total_libros_no_devueltos = 0
    
    return {
            "fecha_generacion": fecha_formateada,
            "total_libros_prestados": total_libros_prestados,
            "total_compras_libros": total_libros_comprados,
            "total_libros_no_devueltos": total_libros_no_devueltos,
        }

def generate_csv_content(report_data):
    """
    Genera el contenido de un archivo CSV a partir de los datos de un informe.
    Args:
        report_data (dict): Diccionario con la información del informe.
    Returns:
        StringIO: Buffer de texto con el contenido del archivo CSV.
    """
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)

    csv_writer.writerow(["Fecha Generacion", "Libros Prestados", "Libros Comprados", "Libros No Devueltos"])

    csv_writer.writerow([report_data["fecha_generacion"], report_data["total_libros_prestados"], report_data["total_compras_libros"], report_data["total_libros_no_devueltos"]])

    return csv_buffer

def generate_csv_content_by_user(report_data, db):
    """
    Genera el contenido de un archivo CSV por usuario a partir de los datos de informes.
    Args:
        report_data (list): Lista de objetos de informes.
        db: Sesión de la base de datos.
    Returns:
        StringIO: Buffer de texto con el contenido del archivo CSV.
    """
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(["Fecha Generacion", "Libros Prestados", "Libros Comprados", "Libros No Devueltos", "Usuario"])

    for informe in report_data:
        fecha_generacion = informe.fechaGeneracion
        libros_prestados = informe.numeroLibrosPrestados
        libros_comprados = informe.numeroComprasLibros
        libros_no_devueltos = informe.numeroLibrosNoDevueltos
        usuario = informe.id_usuario

        usuario = db.query(Usuario).filter(Usuario.id == usuario).first()
        nombre_usuario =    usuario.nombre

        csv_writer.writerow([fecha_generacion, libros_prestados, libros_comprados, libros_no_devueltos, nombre_usuario])

    return csv_buffer

def generate_xlsx_content(report_data):
    """
    Genera el contenido de un archivo XLSX a partir de los datos de un informe.
    Args:
        report_data (dict): Diccionario con la información del informe.
    Returns:
        BytesIO: Buffer de bytes con el contenido del archivo XLSX.
    """
    wb = openpyxl.Workbook()
    ws = wb.active

    ws.append(["Fecha Generacion", "Libros Prestados", "Libros Comprados", "Libros No Devueltos"])

    ws.append([report_data["fecha_generacion"], report_data["total_libros_prestados"], report_data["total_compras_libros"], report_data["total_libros_no_devueltos"]])

    xlsx_buffer = BytesIO()
    wb.save(xlsx_buffer)

    return xlsx_buffer

def generate_xlsx_content_by_user(report_data, db):
    """
    Genera el contenido de un archivo XLSX por usuario a partir de los datos de informes.
    Args:
        report_data (list): Lista de objetos de informes.
        db: Sesión de la base de datos.
    Returns:
        BytesIO: Buffer de bytes con el contenido del archivo XLSX.
    """
    wb = openpyxl.Workbook()
    ws = wb.active

    ws.append(["Fecha Generacion", "Libros Prestados", "Libros Comprados", "Libros No Devueltos", "Usuario"])

    for informe in report_data:
        fecha_generacion = informe.fechaGeneracion
        libros_prestados = informe.numeroLibrosPrestados
        libros_comprados = informe.numeroComprasLibros
        libros_no_devueltos = informe.numeroLibrosNoDevueltos
        usuario = informe.id_usuario

        usuario = db.query(Usuario).filter(Usuario.id == usuario).first()
        nombre_usuario = usuario.nombre

        ws.append([fecha_generacion, libros_prestados, libros_comprados, libros_no_devueltos, nombre_usuario])

    xlsx_buffer = BytesIO()
    wb.save(xlsx_buffer)

    return xlsx_buffer

def generate_pdf_content(report_data):
    """
    Genera el contenido de un archivo PDF a partir de los datos de un informe.
    Args:
        report_data (dict): Diccionario con la información del informe.
    Returns:
        BytesIO: Buffer de bytes con el contenido del archivo PDF.
    """
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)

    pdf.setTitle("Informe General")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 830, "LibraManage - Sistema de Gestión de Bibliotecas")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 800, "Informe General")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(100, 780, "Fecha Generacion")
    pdf.drawString(100, 760, "Libros Prestados")
    pdf.drawString(100, 740, "Libros Comprados")
    pdf.drawString(100, 720, "Libros No Devueltos")

    pdf.drawString(300, 780, str(report_data["fecha_generacion"]))
    pdf.drawString(300, 760, str(report_data["total_libros_prestados"]))
    pdf.drawString(300, 740, str(report_data["total_compras_libros"]))
    pdf.drawString(300, 720, str(report_data["total_libros_no_devueltos"]))

    pdf.showPage()
    pdf.save()

    return pdf_buffer

def generate_pdf_content_by_user(report_data, db):
    """
    Genera el contenido de un archivo PDF por usuario a partir de los datos de informes.
    Args:
        report_data (list): Lista de objetos de informes.
        db: Sesión de la base de datos.
    Returns:
        BytesIO: Buffer de bytes con el contenido del archivo PDF.
    """
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    styles = getSampleStyleSheet()

    data = [["Fecha Generación", "Libros Prestados", "Libros Comprados", "Libros No Devueltos", "Usuario"]]

    for informe in report_data:
        fecha_generacion = str(informe.fechaGeneracion)
        libros_prestados = str(informe.numeroLibrosPrestados)
        libros_comprados = str(informe.numeroComprasLibros)
        libros_no_devueltos = str(informe.numeroLibrosNoDevueltos)
        usuario = informe.id_usuario

        usuario_obj = db.query(Usuario).filter(Usuario.id == usuario).first()
        nombre_usuario = usuario_obj.nombre

        data.append([fecha_generacion, libros_prestados, libros_comprados, libros_no_devueltos, nombre_usuario])

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table = Table(data, style=table_style)

    elements = []
    elements.append(Paragraph("LibraManage - Sistema de Gestión de Bibliotecas", styles['Title']))
    elements.append(Paragraph("Informe General", styles['Heading1']))
    elements.append(table)

    pdf.build(elements)

    return pdf_buffer

def get_report(id: int, db):
    cat = db.query(Report).filter(Report.id == id).first()
    return cat


def update_report(report_id: int, updated_report: Report, db) -> Optional[Report]:
        usr = get_report(report_id, db)
        if usr:
            usr.fechaGeneracion = updated_report.fechaGeneracion
            usr.numeroLibrosPrestados = updated_report.numeroLibrosPrestados
            usr.numeroComprasLibros = updated_report.numeroComprasLibros
            usr.numeroLibrosNoDevueltos = updated_report.numeroLibrosNoDevueltos
            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(usr)
            return usr
        return None


