from flask import g


from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from .errors import *
from .models import Link
from .serializers import LinkSerializer
from .services import make_short_url

from app import db
from app.users.models import User


class PublicUrlShortener(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('long_url', type=str, required=True, help='Missing long_url parameter')
        super(PublicUrlShortener, self).__init__()

    @jwt_optional
    def post(self):
        username = get_jwt_identity()
        data = self.reqparse.parse_args(http_error_code=400)
        serializer = LinkSerializer()
        data['public'] = True
        data['privacy'] = False
        data['short_url'] = make_short_url()
        data['count_of_visits'] = 0
        if username:
            data['user_id'] = User.find_by_username(username).id
        link = Link()
        for k, v in data.items():
            setattr(link, k, v)
        link.check_and_save_link()
        return {'message': 'A shortened url was created successfully', 'link': serializer.dump(link)}
