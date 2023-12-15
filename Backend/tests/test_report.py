from fastapi.testclient import TestClient
import pytest
from app import app

client = TestClient(app)

#crear reporte
'''
def test_create_report():
    response = client.post(
        "/reportcreate/",
                json={
        "fechaGeneracion": "2023-12-03",
        "numeroLibrosPrestados": 3,
        "numeroLibrosNoDevueltos": 5,
        "numeroComprasLibros": 6,
        "id_usuario": 3
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Reporte created successfully" }
'''

#obtener todos los informes
'''
def test_get_all_report():
    response = client.get("/report/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "fechaGeneracion": "2023-12-03",
            "numeroLibrosPrestados": 3,
            "numeroLibrosNoDevueltos": 5,
            "numeroComprasLibros": 6,
            "id_usuario": 3
        }
    ]

#obtener informe por id
def test_get_report():
    response = client.get("/report/1")
    assert response.status_code == 200
    assert response.json() == {
        "fechaGeneracion": "2023-12-03",
        "numeroLibrosPrestados": 3,
        "numeroLibrosNoDevueltos": 5,
        "numeroComprasLibros": 6,
        "id_usuario": 3,
        "id": 1
    }
'''


#descargar csv
'''
def test_download_csv():
    response = client.get("/report/download-csv/")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=report.csv"

#descargar csv de todos los usuarios
def test_download_csv_all_users():
    response = client.get("/report/download-csv-all-users/")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=report_users.csv"

#descargar xlsx
def test_download_xlsx():
    response = client.get("/report/download-xlsx/")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=report.xlsx"

#descargar xlsx de todos los usuarios
def test_download_xlsx_all_users():
    response = client.get("/report/download-xlsx-all-users/")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=report_users.xlsx"

#descargar pdf
def test_download_pdf():
    response = client.get("/report/download-pdf/")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=report.pdf"

#descargar pdf de todos los usuarios
def test_download_pdf_all_users():
    response = client.get("/report/download-pdf-all-users/")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=report_users.pdf"
'''