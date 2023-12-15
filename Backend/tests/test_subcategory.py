from fastapi.testclient import TestClient
import pytest
from app import app

client = TestClient(app)

#crear subcategoria
'''
def test_create_subcategory():
    response = client.post(
        "/new_subcategory/",
        json={
            "nombre": "Terror",
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Subcategoria created successfully" }
    '''

#obtener subcategoria por nombre
'''
def test_get_subcategory():
    response = client.get("/subcategory/Terror")
    assert response.status_code == 200
    assert response.json() == {
        "id": 6,
        "nombre": "Terror",
    }
    '''

#obtener todas las subcategorias
'''
def test_get_all_subcategories():
    response = client.get("/all_subcategories/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "nombre": "Cuento",
        },
        {
            "nombre": "Articulo",
        },
        {
            "nombre": "Terror",
        }
    ]
    '''

#eliminar subcategorias por id
'''
def test_delete_subcategories_id():
    response = client.delete("/delete_subcategories/6")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Subcategoria deleted successfully",
        "subcategoria": {
            "id": 6,
            "nombre": "Terror",
        }
    }
'''