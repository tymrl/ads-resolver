import json
import flask

from resolver import Resolver

app = flask.Flask(__name__)
app.resolver = Resolver()

@app.route('/')
def resolve_refstring():
    """
    A very simple wrapper around our Resolver class to serve an API with the
    desired functionality.
    """
    refstring = flask.request.values.get('refstring', '')
    return flask.jsonify({
        'refstring': refstring,
        'bibcode': app.resolver.make_bibcode(refstring)
    })

def run():
    app.run()
