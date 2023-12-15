from fastapi.testclient import TestClient
import pytest
from app import app

autor = TestClient(app)

"""def test_create_new_autor():
    response = autor.post("/new_author/",json={"nombre": "Gabriel Garcia Marquez"})
    assert response.status_code == 200
    assert response.json() == {"nombre": "Gabriel Garcia Marquez"}
"""

"""def test_getAutor():
    response = autor.get("/author/Gabriel Garcia Marquez")
    assert response.status_code == 200
    assert response.json() == {"nombre": "Gabriel Garcia Marquez", "id": 3}
"""

"""def test_get_allAutors():
    response = autor.get("/all_authors/")
    assert response.status_code == 200
    assert response.json() == [{"nombre": "Antoine de Saint-Exupéry"},
        {"nombre": "Mario Mendoza" },{"nombre": "Gabriel Garcia Marquez"}]
 """   
 
"""def test_delete_author():
    response = autor.delete("/delete_authors/3")
    assert response.status_code == 200
    assert response.json() == {"message": "author deleted successfully"}
"""