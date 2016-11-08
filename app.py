from flask import Flask


app = Flask(__name__)

@app.route('/')
def resolve_refstring():
    return "Hello, World!"
