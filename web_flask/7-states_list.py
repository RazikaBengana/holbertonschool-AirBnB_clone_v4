#!/usr/bin/python3
"""Script to start a Flask web application related to State objects stored in a 'storage'"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """Close the database or file storage system session at the end of each request"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Serve a webpage that lists all State objects sorted by name"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)

    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
