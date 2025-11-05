import pytest
from fastapi.testclient import TestClient
from workout_api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_root(client):
    """Testa se a API está rodando"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API rodando!"}