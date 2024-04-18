#!/usr/bin/python3
"""Script that initializes a Flask application to display states and cities from a database"""

from flask import Flask, render_template
from models import storage
from models.state import State
from os import environ


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """Close the database session at the end of the request or when the application shuts down"""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_state(id=""):
    """
    Serve a web page that lists states or the cities within a specific state, identified by 'id';
    If 'id' is not provided, all states are listed;
    If 'id' is provided but does not match, the result indicates no state found
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    found = 0
    state = ""
    cities = []

    for i in states:
        if id == i.id:
            state = i
            found = 1
            break

    if found:
        states = sorted(state.cities, key=lambda k: k.name)
        state = state.name

    if id and not found:
        found = 2

    return render_template('9-states.html', state=state, array=states, found=found)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
