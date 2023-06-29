import unittest
from fastapi.testclient import TestClient
from main import app  # or wherever your FastAPI application is defined
import json

client = TestClient(app)

class TestRoutes(unittest.TestCase):
    def test_ask2(self):
        # Send a post request to the ask2 route
        response = client.post("/ask2", json={"question": "What is AI?"})
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response data contains the expected keys
        data = response.json()
        self.assertIn('James said', data)

    def test_create_upload_file(self):
        # Open an audio file in binary mode
        with open("output.mp3", "rb") as audio_file:
            # Send a post request to the create_upload_file route
            response = client.post("/uploadfile/",
                                   files={"file": ("filename.mp3", audio_file, "audio/mpeg")})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response data contains the expected keys
        data = response.json()
        self.assertIn('filename', data)
        self.assertIn('transcript', data)
        self.assertIn('response', data)

if __name__ == '__main__':
    unittest.main()
