import json
import requests
from unittest import TestCase

from app import app


class FlaskAppTest(TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_flask_response(self):
        refstring = 'Abt, H. 1990, ApJ, 357, 1'
        response = self.client.get('/?refstring=%s' % refstring)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data.decode('utf-8')),
            {'refstring': refstring,
             'bibcode': '1990ApJ...357....1A'}
        )
