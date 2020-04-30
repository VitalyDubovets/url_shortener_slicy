from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import IntegrityError

from .models import User
from app import db


class UserCollectionAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json', required=True,
                                   help='Username is not specified')
        self.reqparse.add_argument('password', type=str, location='json', required=True,
                                   help='Password is not specified')
        self.reqparse.add_argument('email', type=str, location='json', required=True,
                                   help='Email is not specified')
        super(UserCollectionAPI, self).__init__()

    def get(self):
        return {'msg': 'Hello World'}

    def post(self):
        args = self.reqparse.parse_args(http_error_code=400)
        user = User(username=args['username'], password=args['password'], email=args['email'])
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, kwargs={'message': 'User already exists'})
        return {'message': f'User "{user.username}" created successfully'}, 201


class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        super(UserAPI, self).__init__()

    def get(self, user_id):
        return {'msg': user_id}

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass
