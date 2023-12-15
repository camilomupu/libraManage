from fastapi.testclient import TestClient
import pytest
from app import app

client = TestClient(app)


'''
def test_create_user():
    response = client.post(
        "/register_user/",
        json={
            "nombre": "Pablito Prueba",
            "correo": "pablitoprueba@gmail.com",
            "fechaNacimiento": "2023-12-03",
            "id_rol": 1,
            "contrasena": "Admin12345"

        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario registrado exitosamente"}
'''

#login
'''
def test_login():
    response = client.post(
        "/login_user", params={"correo": "pablitoprueba@gmail.com", "contrasena": "Admin12345"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Ingreso exitoso"}


#obtener todos los usuarios
def test_get_all_users():
    response = client.get("/all_users/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
'''

'''
def test_get_fines_and_deadlines():
    response = client.get("/management_fine/", params={"id_prestamo": 1, "correo_usuario": "pablitoprueba@gmail.com", "id_usuario_prestamo": 4})
    assert response.status_code == 404
    assert response.json() == {"detail": "User has no loans"}
'''


