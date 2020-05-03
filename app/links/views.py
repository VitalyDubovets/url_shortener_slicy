from flask import g

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from flask_restful import Resource, reqparse
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .errors import *
from .models import Link
from .serializers import LinkSerializer
from .services import make_short_url

from app.users.models import User


class AuthUrlShortenerCollectionAPI(Resource):
    method_decorators = [jwt_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('long_url', type=str, required=True, help='Missing long_url parameter')
        self.reqparse.add_argument('short_url', type=str, default=make_short_url())
        self.reqparse.add_argument('public', type=bool, default=False)
        self.reqparse.add_argument('privacy', type=bool, default=False)
        super(AuthUrlShortenerCollectionAPI, self).__init__()

    def get(self, user_id):
        links = Link.query.filter(or_(Link.user_id == user_id, Link.public == True)).all()
        serializer = LinkSerializer(many=True)
        return serializer.dump(links)

    def post(self, user_id):
        data = self.reqparse.parse_args(http_error_code=400)
        data['user_id'] = user_id
        link = Link()
        serializer = LinkSerializer()
        for k, v in data.items():
            setattr(link, k, v)
        try:
            link.check_and_save_link()
        except IntegrityError:
            link.short_url = make_short_url(9)
            link.check_and_save_link()
        return {'message': 'A closed short url was created successfully.', 'link_info': serializer.dump(link)}


class PublicUrlShortenerCollectionAPI(Resource):
    method_decorators = [jwt_optional]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('long_url', type=str, required=True, help='Missing long_url parameter')
        super(PublicUrlShortenerCollectionAPI, self).__init__()

    def get(self):
        links = Link.query.filter_by(public=True)
        serializer = LinkSerializer(many=True)
        return serializer.dump(links)

    def post(self):
        username = get_jwt_identity()
        data = self.reqparse.parse_args(http_error_code=400)
        serializer = LinkSerializer()
        data['public'] = True
        data['privacy'] = False
        data['short_url'] = make_short_url()
        if username:
            data['user_id'] = User.find_by_username(username).id
        link = Link()
        for k, v in data.items():
            setattr(link, k, v)
        try:
            link.check_and_save_link()
        except IntegrityError:
            link.short_url = make_short_url(9)
            link.check_and_save_link()
        return {'message': 'A shortened url was created successfully', 'link_info': serializer.dump(link)}
