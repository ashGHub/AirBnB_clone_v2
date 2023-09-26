#!/usr/bin/python3
"""Start a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Display Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Display C followed by the value of the text variable"""
    return f"C {text.replace('_', ' ')}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
