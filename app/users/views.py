import datetime

from flask import g
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required,
                                get_jwt_identity, jwt_required, get_raw_jwt)
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from .errors import *
from .models import User, BlacklistToken
from .serializers import UserSerializer

from app import db, jwt


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return BlacklistToken.is_jti_blacklisted(jti)


class AuthAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='Missing username parameter')
        self.reqparse.add_argument('password', type=str, required=True, help='Missing password parameter')
        super(AuthAPI, self).__init__()

    def post(self):
        data = self.reqparse.parse_args()
        current_user = User.find_by_username(data['username'])
        if not current_user or not current_user.check_password(data['password']):
            raise BadUsernameOrPasswordError
        access_expiry = datetime.timedelta(minutes=15)
        refresh_expiry = datetime.timedelta(days=30)
        access_token = create_access_token(identity=current_user.username, expires_delta=access_expiry)
        refresh_token = create_refresh_token(identity=current_user.username, expires_delta=refresh_expiry)
        g.user = current_user
        # set_access_cookies(resp, access_token)
        return {
            'message': f"Logged in as {current_user.username}",
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


class UserCollectionAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json', required=True,
                                   help='Missing username parameter')
        self.reqparse.add_argument('password', type=str, location='json', required=True,
                                   help='Missing password parameter')
        self.reqparse.add_argument('email', type=str, location='json', required=True,
                                   help='Missing email parameter')
        super(UserCollectionAPI, self).__init__()

    @jwt_required
    def get(self):
        serializer = UserSerializer(many=True)
        users = User.query.all()
        return serializer.dump(users), 200

    def post(self):
        data = self.reqparse.parse_args(http_error_code=400)
        user = User(username=data['username'], password=data['password'], email=data['email'])
        serializer = UserSerializer()
        access_expiry = datetime.timedelta(minutes=15)
        refresh_expiry = datetime.timedelta(days=30)
        access_token = create_access_token(identity=user.username, expires_delta=access_expiry)
        refresh_token = create_refresh_token(identity=user.username, expires_delta=refresh_expiry)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            raise UserAlreadyExistsError
        return {
            'message': f"User {user.username} was created successfully",
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': serializer.dump(user)
        }, 201


class UserAPI(Resource):
    method_decorators = [jwt_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        super(UserAPI, self).__init__()

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserDoesNotExistError
        serializer = UserSerializer()
        return serializer.dump(user)

    def patch(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserDoesNotExistError
        data = self.reqparse.parse_args()
        updated_data = data.copy()
        for k, v in data.items():
            if not v:
                updated_data.pop(k)
        if not updated_data:
            raise ArgumentsIsEmptyError
        serializer = UserSerializer()
        for k, v in updated_data.items():
            setattr(user, k, v)
        db.session.add(user)
        db.session.commit()
        return {'updated_data': updated_data, 'user': serializer.dump(user)}, 200

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserIsAlreadyDeletedError
        serializer = UserSerializer()
        user_data = serializer.dump(user)
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User deleted successfully.', 'user': user_data}, 204


class UserLogoutAccessAPI(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_token = BlacklistToken(jti=jti)
        revoked_token.add_token_to_blacklist()
        return {'message': 'Access token has been revoked'}


class UserLogoutRefreshAPI(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_token = BlacklistToken(jti=jti)
        revoked_token.add_token_to_blacklist()
        return {'message': 'Refresh token has been revoked'}


class TokenRefreshAPI(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_expiry = datetime.timedelta(minutes=15)
        access_token = create_access_token(identity=current_user, expires_delta=access_expiry)
        return {'access_token': access_token}, 200
