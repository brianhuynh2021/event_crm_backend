from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_filter_events_by_owner():
    response = client.get("/api/v1/events/filter", params={"owner": "user_123"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert all(event["owner"] == "user_123" for event in data)