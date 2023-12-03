#FALTA AJUSTAR LAS PRUEBAS DE OBTENER TODO Y LA DE REGRESAR EL PRESTAMO
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

'''
def test_create_new_loan():
    response = client.post(
        "/new_loan/",
        json={
            "fechaPrestamo": "2023-06-01", "id_usuario": 3, "id_libroFisico": 9
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Loan created successfully"}
'''

#obtener prestamos por id usuario, id libro y fecha
'''
def test_get_loan():
    response = client.get("/loan/3/9/{date}?date_loan=2023-06-01")
    assert response.status_code == 200
    #assert "id" in response.json()
    assert response.json() == [
  {
    "fechaPrestamo": "2023-06-01",
    "id": 2,
    "id_usuario": 3,
    "fechaVencimiento": "2023-06-04",
    "devuelto": True,
    "id_libroFisico": 9
  }
]
'''

'''
#obtener disponibilidad por id libro y fecha
def test_get_availability():
    response = client.get("/check_availability/9/2023-06-01")
    assert response.status_code == 200
    #assert "id" in response.json()
    assert response.json() == [
  {
    "fechaPrestamo": "2023-06-01",
    "id": 2,
    "id_usuario": 3,
    "fechaVencimiento": "2023-06-04",
    "devuelto": True,
    "id_libroFisico": 9
  }
]
'''

#obtener todos los prestamos
'''
def test_get_all_loan():
    response = client.get("/all_loans/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

#obtener prestamo po nombre y fecha
'''

'''
def test_return_loan_by_book_name_and_date():
    response = client.put("/return_loan_by_book_name_and_date/", params={"book_name": "El  principito", "loan_date": "2023-06-01"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "id_usuario": 3, "id_libroFisico": 9, "fechaPrestamo": "2023-06-01"}
'''

#eliminar prestamo por id
'''
def test_delete_loan():
    response = client.delete("/delete_loan/2")
    assert response.status_code == 200
    #assert "message" in response.json()
    assert response.json() == {"message": "Loan deleted successfully"}
'''