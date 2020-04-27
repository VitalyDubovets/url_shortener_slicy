from app import api

from .views import UserAPI


api.add_resource(UserAPI, '/users/<int:id>', endpoint='user')
