import json

import flask

app = flask.Flask(__name__)

@app.route('/')
def resolve_refstring():
    refstring = flask.request.values.get('refstring')
    return flask.jsonify({
        'refstring': refstring,
        'bibcode': '1990ApJ...357....1A'
    })
