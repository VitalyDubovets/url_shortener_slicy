from flask import Blueprint
from flask_restful import Api

from .errors import errors
from .views import *


users = Blueprint('users', __name__)
api_users = Api(users, prefix='/api/v1', errors=errors)

api_users.add_resource(AuthAPI, '/auth/', endpoint='authorization')
api_users.add_resource(UserLogoutAccessAPI, '/logout/access/', endpoint='logout access')
api_users.add_resource(UserLogoutRefreshAPI, '/logout/refresh/', endpoint='logout refresh')
api_users.add_resource(UserCollectionAPI, '/users/', endpoint='user_collection')
api_users.add_resource(UserAPI, '/users/<int:user_id>/', endpoint='user')
api_users.add_resource(TokenRefreshAPI, '/token/refresh/', endpoint='token refresh')

from . import *
