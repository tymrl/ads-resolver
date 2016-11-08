import requests
from unittest import TestCase

from app import app


class FlaskAppTest(TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_flask_response(self):
        self.assertEqual(self.client.get('/').status_code, 200)
