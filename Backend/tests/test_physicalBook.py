from fastapi.testclient import TestClient
from app import app
import pytest

client = TestClient(app)
'''
def test_create_new_physicalBook():
    response = client.post(
        "/register_physicalBooks/",
        params={
            "correo": "jefferhenao911@gmail.com","titulo": "Cien años de soledad", "descripcion": "Libro de Gabriel Garcia Marquez",
            "ubicacion": "Biblioteca Central", "estado": "Disponible", "id_autor": 3, "id_categoria": 1, "id_subcategoria": 1,  "url_image": "https://www.lamusica.com.co/cdn/shop/products/img20230111_12074440.jpg?v=1673457099",
        }
    )

    assert response.status_code == 200

    #assert "id" in response.json()
    assert response.json() == {"message": "Physical book created successfully"}
'''

#obtener libro fisico por titulo
'''
def test_get_physicalBook():
    response = client.get("/book/Cien años de soledad/3")
    assert response.status_code == 200
    assert response.json() == {
            "titulo": "Cien años de soledad", "descripcion": "Libro de Gabriel Garcia Marquez", "portada": "https://www.lamusica.com.co/cdn/shop/products/img20230111_12074440.jpg?v=1673457099",
            "ubicacion": "Biblioteca Central", "estado": "Disponible", "id_autor": 3, "id_subcategoria": 1, "id_categoria": 1, "id": 10
        }
'''
    
#obtener todos los libros fisicos
'''
def test_get_all_physicalBook():
    response = client.get("/all_physicalBooks/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
'''

#eliminar libro fisico por id
'''
def test_delete_physicalBook():
    response = client.delete("/delete_physicalBook/10")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json() == {"message": "Physical book deleted successfully"}
'''

'''
def test_serach_physicalBook():
    response = client.get(
        "/search_physicalBook/", params={"titulo": "El  principito"})
    assert response.status_code == 200
    assert response.json() == [
                {
            "descripcion": "El Principito, es una novela corta escrita por Antoine de Saint-Exupéry. Publicada en 1943, la historia sigue las aventuras de un pequeño príncipe que viaja por diferentes planetas, explorando temas como la amistad, el amor y la naturaleza humana. A través de encuentros con diversos personajes, el libro aborda reflexiones filosóficas sobre la vida y la importancia de ver el mundo con los ojos del corazón.",
            "portada": "https://images.cdn2.buscalibre.com/fit-in/360x360/1a/d0/1ad00b45cfb9ee36f629b922d55ced81.jpg",
            "estado": "Disponible",
            "id_subcategoria": 1,
            "id_categoria": 1,
            "id": 9,
            "titulo": "El  principito",
            "ubicacion": "A-1",
            "id_autor": 1
        }
    ]
'''