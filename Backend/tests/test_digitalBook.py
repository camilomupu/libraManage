from fastapi.testclient import TestClient
import pytest
from app import app

digitalBook = TestClient(app)

"""def test_register_digitalBook():
    response = digitalBook.post("/register_digitalBooks/", params={"correo":"dany.1701627413@ucaldas.edu.co",
                                                                    "titulo":"Cien años de soledad",
                                                                    "descripcion":"Cien años de soledad, es una novela escrita por el autor colombiano Gabriel García Márquez. Publicada en 1967, la historia narra la saga de la familia Buendía en el ficticio pueblo de Macondo. ",
                                                                    "precio":30000,
                                                                    "id_autor":3,
                                                                    "id_categoria":1,
                                                                    "id_subcategoria":1,
                                                                    "url_image":"https://www.lamusica.com.co/cdn/shop/products/img20230111_12074440.jpg?v=1673457099",
                                                                    "link_libro":"https://www.secst.cl/upfiles/documentos/02072019_916am_5d1b755b8c54f.pdf"})   
    assert response.status_code == 200
    assert response.json() == {"message": "Digital book created successfully"}
  """


"""def test_get_digitalBook():
    response = digitalBook.get("/digitalBook/Cien años de soledad/3")
    assert response.status_code == 200
    assert response.json() == {
        "titulo": "Cien años de soledad",
        "portada": "https://www.lamusica.com.co/cdn/shop/products/img20230111_12074440.jpg?v=1673457099",
        "descripcion": "Cien años de soledad, es una novela escrita por el autor colombiano Gabriel García Márquez. Publicada en 1967, la historia narra la saga de la familia Buendía en el ficticio pueblo de Macondo. ",
        "link_Libro": "https://www.secst.cl/upfiles/documentos/02072019_916am_5d1b755b8c54f.pdf",
        "precio": 30,
        "id_autor": 3,
        "id_subcategoria": 1,
        "id_categoria": 1,
        "id": 2
    }"""

"""
def test_get_all_digitalBook():
    response = digitalBook.get("/all_digitalBooks/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "titulo": "La bella y la bestia",
            "portada": "https://es.web.img2.acsta.net/c_310_420/pictures/17/01/09/09/56/256507.jpg",
            "descripcion": "La Bella y la Bestia, es un cuento de hadas clásico que ha sido adaptado en diversas formas a lo largo de la historia. La historia gira en torno a una joven llamada Bella, que sacrifica su libertad para vivir en un castillo con una criatura encantada, la Bestia. ",
            "link_Libro": "https://www.icbf.gov.co/sites/default/files/22_lemc_bella_y_la_bestia_compressed.pdf",
            "precio": 10000,
            "id_autor": 1,
            "id_subcategoria": 1,
            "id_categoria": 1
        },
        {
            "titulo": "Cien años de soledad",
            "portada": "https://www.lamusica.com.co/cdn/shop/products/img20230111_12074440.jpg?v=1673457099",
            "descripcion": "Cien años de soledad, es una novela escrita por el autor colombiano Gabriel García Márquez. Publicada en 1967, la historia narra la saga de la familia Buendía en el ficticio pueblo de Macondo. ",
            "link_Libro": "https://www.secst.cl/upfiles/documentos/02072019_916am_5d1b755b8c54f.pdf",
            "precio": 30,
            "id_autor": 3,
            "id_subcategoria": 1,
            "id_categoria": 1
        }
    ]
"""

"""def test_delete_digitalBook():
    response = digitalBook.delete("/delete_digitalBook/6")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Digital book deleted successfully"
    }"""


"""def test_serach_digitalBook():
    response = digitalBook.get(
        "/search_digitalBook/", params={"titulo": "Cien años de soledad"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 7,
            "link_Libro": "https://www.secst.cl/upfiles/documentos/02072019_916am_5d1b755b8c54f.pdf",
            "precio": 30000,
            "id_subcategoria": 1,
            "titulo": "Cien años de soledad",
            "portada": "https://www.lamusica.com.co/cdn/shop/products/img20230111_12074440.jpg?v=1673457099",
            "descripcion": "Cien años de soledad, es una novela escrita por el autor colombiano Gabriel García Márquez. Publicada en 1967, la historia narra la saga de la familia Buendía en el ficticio pueblo de Macondo. ",
            "id_autor": 3,
            "id_categoria": 1
        }
    ]"""
