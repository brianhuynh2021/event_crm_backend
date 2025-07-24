import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestUserFilterAPI(unittest.TestCase):

    def test_filter_users_by_company(self):
        response = client.get("/api/v1/users/filter", params={"company": "Grab"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(all("Grab" in user.get("company", "") for user in data))

    def test_filter_users_by_job_title_and_city(self):
        response = client.get(
            "/api/v1/users/filter", 
            params={"job_title": "AI Engineer", "city": "Singapore"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        for user in data:
            self.assertEqual(user.get("job_title"), "AI Engineer")
            self.assertEqual(user.get("city"), "Singapore")

    def test_pagination_and_sorting(self):
        response = client.get(
            "/api/v1/users/filter",
            params={"skip": 0, "limit": 2, "sort_by": "first_name", "sort_dir": "asc"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertLessEqual(len(data), 2)
        if len(data) == 2:
            self.assertLessEqual(data[0]["first_name"], data[1]["first_name"])

    def test_filter_no_match(self):
        response = client.get("/api/v1/users/filter", params={"company": "NoSuchCompanyXYZ"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])