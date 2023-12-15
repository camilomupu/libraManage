from fastapi.testclient import TestClient
import pytest
from app import app

category = TestClient(app)


"""def test_create_category():
    response = category.post("/new_category/", json={"nombre": "Drama"})
    assert response.status_code == 200
    assert response.json() == {"nombre": "Drama"}"""
    
"""def test_get_category_nombre():
    response = category.get("/category/Drama")
    assert response.status_code == 200
    assert response.json() == {"nombre": "Drama", "id":4}"""
    
"""def test_get_allCategories():
    response = category.get("/all_categories/")
    assert response.status_code == 200
    assert response.json() == [{"nombre": "Ficción"},{"nombre": "Terror"},{"nombre": "Ciencia"},{"nombre": "Drama"}]
"""

"""def test_delete_category():
    response = category.delete("/delete_categories/4")
    assert response.status_code == 200
    assert response.json() == {"message": "Categoria deleted successfully", "categoria": {"nombre": "Drama"}}
"""


