from fastapi.testclient import TestClient
import pytest
from app import app

fine = TestClient(app)


"""def test_new_fine():
    response = fine.post("/new_fine/", json={
        "valorDeuda": 10000,
        "estadoMulta": 1,
        "fechaDePago": "2023-12-03",
        "id_prestamo": 1
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Fine created successfully"}
"""


"""def test_get_fine_id():
    response = fine.get("/fine/1")
    assert response.status_code == 200
    assert response.json() == {
        "valorDeuda": 10000,
        "estadoMulta": 1,
        "fechaDePago": "2023-12-03",
        "id_prestamo": 1,
        "id": 1
    }
 """


"""def test_get_allFines():
    response = fine.get("/all_finee/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "estadoMulta": 1,
            "valorDeuda": 10000,
            "fechaDePago": "2023-12-03",
            "id_prestamo": 1
        }
    ]
"""
"""def test_pay_fine():
    response = fine.put("/pay_fine/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Fine paid successfully"}
"""

"""def test_forgive_fine():
    response = fine.put("/forgive_fine/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Fine forgiven successfully"}
"""

"""def test_delete_fine():
    response = fine.delete("/delete_fine/3")
    assert response.status_code == 200
    assert response.json() == {"message": "Fine deleted successfully"}
"""


