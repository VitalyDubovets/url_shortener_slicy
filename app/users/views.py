from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import IntegrityError

from .models import User
from .serializers import UserSerializer
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
        serializer = UserSerializer(many=True)
        users = User.query.all()
        return serializer.dump(users), 200

    def post(self):
        args = self.reqparse.parse_args(http_error_code=400)
        user = User(username=args['username'], password=args['password'], email=args['email'])
        serializer = UserSerializer()
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message='User already exists')
        return {'message': f'User created successfully.',
                'user': serializer.dump(user)}, 201


class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        super(UserAPI, self).__init__()

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(400, message="User doesn't exist")
        serializer = UserSerializer()
        return serializer.dump(user)

    def patch(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(400, message="User doesn't exist")
        args = self.reqparse.parse_args()
        updated_data = args.copy()
        for k, v in args.items():
            if not v:
                updated_data.pop(k)
        if not updated_data:
            abort(400, message='Arguments is empty in json')
        serializer = UserSerializer()
        for k, v in updated_data.items():
            setattr(User, k, v)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message='A user with this name or email already exists')
        return {'updated_data': updated_data, 'user': serializer.dump(user)}, 200

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(400, message="User is already deleted")
        serializer = UserSerializer()
        user_data = serializer.dump(user)
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User deleted successfully.', 'user': user_data}, 204
