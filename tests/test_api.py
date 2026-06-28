from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_page_zero():
    # nao esquecer as chavetas porque estamos a criar um dicionario dentro do get
    # chamo a api com page=0 e como é invalido(page >=1 obrigatoriamente), retorno status code 422
    response = client.get("/job_offers", params={"page": 0})
    assert response.status_code == 422


def test_limit_zero():
    response = client.get("/job_offers", params={"limit": 0})
    assert response.status_code == 422


def test_limit_above_max():
    response = client.get("/job_offers", params={"limit": 51})
    assert response.status_code == 422



