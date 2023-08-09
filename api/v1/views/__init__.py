#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.streets import *
from api.v1.views.lodges import *
from api.v1.views.lodges_reviews import *
from api.v1.views.locations import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.lodges_amenities import *
