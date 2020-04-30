from flask import Blueprint
from flask_restful import Api

from .views import UserAPI, UserCollectionAPI


users = Blueprint('users', __name__)
api_users = Api(users, prefix='/api/v1')

api_users.add_resource(UserCollectionAPI, '/users/', endpoint='user_collection')
api_users.add_resource(UserAPI, '/users/<int:user_id>', endpoint='user')

from . import *
