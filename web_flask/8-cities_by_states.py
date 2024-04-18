#!/usr/bin/python3
"""Script that initializes a Flask web application to display states and cities from storage"""

from flask import Flask, render_template
from models import storage
from models.state import State
from os import environ


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """Close the current SQLAlchemy session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Serve a webpage that lists all states stored in alphabetical order"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)

    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_list():
    """Serve a webpage that lists states along with their cities, both sorted alphabetically"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    return render_template('8-cities_by_states.html', states=st_ct, h_1="States")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
