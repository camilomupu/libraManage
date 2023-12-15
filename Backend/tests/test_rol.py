from fastapi.testclient import TestClient
from app import app
import pytest

client = TestClient(app)

'''
def test_create_new_rol():
    response = client.post(
        "/rolcreate/",
        json={
            "nombre": "Camionero",
        }
    )

    assert response.status_code == 200

    assert "id" in response.json()
    assert response.json()["nombre"] == "Camionero"
'''

'''
def test_get_rol():
    response = client.get("/rol/Camionero")
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["nombre"] == "Camionero"
'''

'''
def test_get_all_roles():
    response = client.get("/all_roles/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
'''

'''
def test_delete_rol():
    response = client.delete("/rol/delete/4")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "User deleted successfully"
'''