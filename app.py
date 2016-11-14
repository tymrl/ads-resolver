import json

import flask

from resolver import Resolver

app = flask.Flask(__name__)
app.resolver = Resolver()

@app.route('/')
def resolve_refstring():
    refstring = flask.request.values.get('refstring')
    return flask.jsonify({
        'refstring': refstring,
        'bibcode': app.resolver.make_bibcode(refstring)
    })
