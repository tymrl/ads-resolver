import requests
from nose.tools import eq_
from unittest import TestCase

from ads_resolver import setup_flask_app


class FlaskAppTest(TestCase):
    def setUp(self):
        app = setup_flask_app()
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_flask_response(self):
        assert '404 Not Found' in self.client.get('/').data
