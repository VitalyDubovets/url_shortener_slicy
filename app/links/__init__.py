from flask import Blueprint
from flask_restful import Api

from .errors import errors
from .views import *


links = Blueprint('links', __name__)
api_links = Api(links, prefix='/api/v1', errors=errors)

api_links.add_resource(PublicUrlShortener, '/links', endpoint='public shortener')

from . import *

