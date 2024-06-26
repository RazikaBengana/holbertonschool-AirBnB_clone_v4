#!/usr/bin/python3
"""Script to initialize a Flask web application for handling state, city, and amenity data"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from os import environ


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """Close the database session at the end of the request or when the application shuts down"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filter():
    """Serve a web page that allows users to filter locations and amenities for HBNB dynamically"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    return render_template('10-hbnb_filters.html',
                           states=st_ct,
                           amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
