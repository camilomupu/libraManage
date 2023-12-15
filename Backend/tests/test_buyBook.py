from fastapi.testclient import TestClient
import pytest
from app import app

buyBook = TestClient(app)


"""def test_new_buyBook():
    response = buyBook.post(
        "/new_buyBook/", json={"id_usuario": 1, "id_libroDigital": 7})
    assert response.status_code == 200
    assert response.json() == {"message": "Buy digital book created successfully"}
"""

"""def test_get_buyBook():
    response = buyBook.get("/buyBook/1/1")
    assert response.status_code == 200
    assert response.json() == {
        "id_usuario": 1,
        "id_libroDigital": 1,
        "id": 1
    }"""


"""def test_all_buyBooks():
    response = buyBook.get("/all_buyBooks/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id_usuario": 1,
            "id_libroDigital": 1
        }
    ]"""
    

"""def test_delete_buyBook_id():
    response = buyBook.delete("/delete_buyBook/1")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Buy digital book deleted successfully"
    }"""

