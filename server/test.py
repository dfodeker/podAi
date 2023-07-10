import unittest
import requests
import json

class TestAsk2Endpoint(unittest.TestCase):
    BASE_URL = 'http://localhost:8000'  # replace  server address and port

    def test_ask2_correct_response(self):
        question = "Who won the world series in 2020?"
        response = requests.post(f"{self.BASE_URL}/ask2", data=json.dumps({'question': question}), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('James said', data)

    def test_ask2_no_question(self):
        response = requests.post(f"{self.BASE_URL}/ask2", data=json.dumps({}), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)  # assuming your API returns a 400 status code for bad requests

    def test_ask2_non_string_question(self):
        question = 12345
        response = requests.post(f"{self.BASE_URL}/ask2", data=json.dumps({'question': question}), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)  # assuming your API returns a 400 status code for bad requests


if __name__ == '__main__':
    unittest.main()

