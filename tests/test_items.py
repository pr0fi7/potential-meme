from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_and_get_item():
    r = client.post("/items", json={"name": "pytest-item"})
    assert r.status_code == 201
    data = r.json()
    assert data["id"] >= 1
    assert data["name"] == "pytest-item"
    assert "created_at" in data


    r2 = client.get(f"/items/{data['id']}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "pytest-item"


def test_list_items():
    r = client.get("/items")
    assert r.status_code == 200
    assert isinstance(r.json(), list)




def test_validation():
    r = client.post("/items", json={"name": ""})
    assert r.status_code == 422