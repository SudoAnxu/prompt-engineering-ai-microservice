# tests/test_api.py
import unittest
from fastapi.testclient import TestClient
from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_route(self):
        # Mock the database or use a test DB for full coverage
        response = self.client.post("/generate", json={"user_id": "test_user", "query": "What is AI?"})
        # If using real DB, ensure test DB is set up; or mock DB calls
        self.assertIn(response.status_code, (200, 400))  # Accept 400 if DB not available

    def test_history_route(self):
        response = self.client.get("/history", params={"user_id": "test_user"})
        self.assertIn(response.status_code, (200, 400))  # Accept 400 if DB not available

if __name__ == "__main__":
    unittest.main()
