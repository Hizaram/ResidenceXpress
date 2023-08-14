#!/usr/bin/python3
""" Starts a Flash Web Application """
from api.v1.views import app_views
from models import storage
from models.location import Location
from models.street import Street
from models.amenity import Amenity
from models.lodge import Lodge
from os import environ
from flask import Flask, render_template
import requests
import uuid
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

def get_lodge_details(lodge_id):
    """Gets the lodge details"""
    api_url = "http://127.0.0.1:5000/api/v1/lodges/{}".format(lodge_id)
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()
    return None

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
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

    #for lodge in lodges:
        #lodge_list.append([lodge, sorted(lodges, key=lambda k: k.name)])

    return render_template('index.html',
                           locations=lc_st,
                           amenities=amenities,
                           lodges=lodges,
                           cache_id=uuid.uuid4())


@app.route('/view_lodge/<lodge_id>', strict_slashes=False)
def view_lodge(lodge_id):
    """Gets and renders the lodge details page"""
    lodge_details = get_lodge_details(lodge_id)

    if lodge_details:
        return render_template('view_lodge.html',
                                lodge=lodge_details)

    return


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
