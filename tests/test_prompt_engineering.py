from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
import unittest

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("main.generate_responses")  
    def test_generate_and_history(self, mock_generate):
        # Mock the generate_responses function to avoid actual API calls
        # and database interactions
        mock_generate.return_value = ("casual answer", "formal answer")

        response = self.client.post("/generate", json={"user_id": "integration_user", "query": "Explain gravity"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["casual_response"], "casual answer")
        self.assertEqual(data["formal_response"], "formal answer")

if __name__ == "__main__":
    unittest.main()
