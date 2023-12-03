from fastapi.testclient import TestClient
import pytest
from app import app

book = TestClient(app)


def test_search_book():
    response = book.get("/search_book/", params={"titulo": "El  principito",
                                                 "categoria": "Ficción", "subcategoria": "Cuento", "autor": "Antoine de Saint-Exupéry"})
    assert response.status_code == 200
    """assert response.json() == {
    "id": 9,
    "descripcion": "El Principito, es una novela corta escrita por Antoine de Saint-Exupéry. Publicada en 1943, la historia sigue las aventuras de un pequeño príncipe que viaja por diferentes planetas, explorando temas como la amistad, el amor y la naturaleza humana. A través de encuentros con diversos personajes, el libro aborda reflexiones filosóficas sobre la vida y la importancia de ver el mundo con los ojos del corazón.",
    "ubicacion": "A-1",
    "id_autor": 1,
    "id_categoria": 1,
    "titulo": "El  principito",
    "portada": "https://images.cdn2.buscalibre.com/fit-in/360x360/1a/d0/1ad00b45cfb9ee36f629b922d55ced81.jpg",
    "estado": "Disponible",
    "id_subcategoria": 1
  }"""

    
