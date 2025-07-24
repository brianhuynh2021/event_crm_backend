from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_filter_users_by_company():
    response = client.get("/api/v1/users/filter", params={"company": "Grab"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("Grab" in user.get("company", "") for user in data)


def test_filter_users_by_job_title_and_city():
    response = client.get(
        "/api/v1/users/filter", 
        params={"job_title": "AI Engineer", "city": "Singapore"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for user in data:
        assert user.get("job_title") == "AI Engineer"
        assert user.get("city") == "Singapore"


def test_pagination_and_sorting():
    response = client.get(
        "/api/v1/users/filter",
        params={"skip": 0, "limit": 2, "sort_by": "first_name", "sort_dir": "asc"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2
    if len(data) == 2:
        assert data[0]["first_name"] <= data[1]["first_name"]
        
def test_filter_no_match():
    response = client.get("/api/v1/users/filter", params={"company": "NoSuchCompanyXYZ"})
    assert response.status_code == 200
    data = response.json()
    assert data == []