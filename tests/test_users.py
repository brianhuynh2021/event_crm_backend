from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_filter_users_by_company():
    response = client.get("/users", params={"company": "Grab"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("Grab" in user["company"] for user in data)

def test_filter_users_by_job_title_and_city():
    response = client.get("/users", params={"job_title": "AI Engineer", "city": "Singapore"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(user["job_title"] == "AI Engineer" and user["city"] == "Singapore" for user in data)

def test_pagination_and_sorting():
    response = client.get("/users", params={"skip": 0, "limit": 2, "sort_by": "first_name", "sort_dir": "asc"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2