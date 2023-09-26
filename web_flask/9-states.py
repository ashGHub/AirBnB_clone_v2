#!/usr/bin/python3
"""Start a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Display Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/states', strict_slashes=False)
def states():
    """Displays an HTML page with a list of all states"""
    states = storage.all(State)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Displays an HTML page with a list of all states"""
    states = storage.all(State)
    state = states.get('State.' + id)
    return render_template('9-states.html', states=states, state=state, id=id)


@app.teardown_appcontext
def teardown_appcontext(exception):
    # Perform teardown actions here
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
