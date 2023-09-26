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


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays an HTML page with a list of all states"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_appcontext(exception):
    # Perform teardown actions here
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
