#!/usr/bin/python3
"""
This script initializes a Flask application to serve a dynamic web page
that displays data from a storage system based on various models
"""

from flask import Flask, render_template
import uuid
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """Close the database session at the end of the request or when the application shuts down"""
    storage.close()


@app.route('/3-hbnb', strict_slashes=False)
def hbnb():
    """Handle routing for the '/3-hbnb' route, fetch and sort data models, then render to '3-hbnb.html'"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []
    cache_id = str(uuid.uuid4())

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template('3-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=cache_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
