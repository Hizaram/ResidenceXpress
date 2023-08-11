#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.location import Location
from models.street import Street
from models.amenity import Amenity
from models.lodge import Lodge
from os import environ
from flask import Flask, render_template
import uuid
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/resixpress/', strict_slashes=False)
def resixpress():
    """ ResidenceXpress is alive! """
    locations = storage.all(Location).values()
    locations = sorted(locations, key=lambda k: k.name)
    lc_st = []

    for location in locations:
        lc_st.append([location, sorted(location.streets, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    lodges = storage.all(Lodge).values()
    lodges = sorted(lodges, key=lambda k: k.name)

    return render_template('index.html',
                           locations=lc_st,
                           amenities=amenities,
                           lodges=lodges,
                           cache_id=uuid.uuid4())


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
