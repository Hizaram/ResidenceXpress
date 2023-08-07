""" Starts a Flash Web Application """
from models import storage
from models.street import Street
from models.location import Location
from models.amenity import Amenity
from models.lodge import Lodge
from models.review import Review
from models.user import User
from os import environ
from flask import Flask, render_template
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filter():
    """ HBNB filters """
    locations = storage.all(Location).values()
    locations = sorted(locations, key=lambda k: k.name)
    loc_ct = []

    for location in locations:
        loc_ct.append([location, sorted(location.streets, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    return render_template('10-hbnb_filters.html',
                           locations=loc_ct,
                           amenities=amenities)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
