import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from main import app  # replace this with actual filename

class TestFastAPIApp(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)

    @patch('openai.ChatCompletion.create')
    def test_ask2(self, mock_create):
        # Mock the response from the openai API
        mock_create.return_value = Mock(choices=[Mock(message={"content": "Mock response"})])

        response = self.client.get("/ask2?question=Test question")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"James said": "Mock response"})


    @patch('requests.post')
    def test_text_to_speech(self, mock_post):
        # Mock the response from the Eleven Labs API
        mock_post.return_value = Mock(status_code=200)

        response = self.client.get("/textToSpeech", json={"speak": "Test Speech"})

        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()