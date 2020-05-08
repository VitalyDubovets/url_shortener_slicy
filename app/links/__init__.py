from flask import Blueprint
from flask_restful import Api

from .errors import errors
from .views import *


links = Blueprint('links', __name__)
api_links = Api(links, prefix='/api/v1', errors=errors)

api_links.add_resource(PublicUrlShortenerCollectionAPI, '/links', endpoint='public shortener')
api_links.add_resource(AuthUrlShortenerCollectionAPI, '/users/<int:user_id>/links', endpoint='auth shortener')
api_links.add_resource(UrlShortenerAPI, '/users/<int:user_id>/links/<int:link_id>')

from . import *

