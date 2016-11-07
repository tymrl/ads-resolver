from flask import Flask


def setup_flask_app():
    """
    Start a Flask app.  Use a function so that we can make a separate one for
    tests.
    """
    return Flask(__name__)


app = setup_flask_app()
