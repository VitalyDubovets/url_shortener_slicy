from flask import g

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from flask_restful import Resource, reqparse
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .errors import *
from .models import Link
from .serializers import LinkSerializer
from .services import make_short_url

from app import db
from app.users.models import User


class UrlShortenerAPI(Resource):
    method_decorators = [jwt_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('long_url', type=str)
        self.reqparse.add_argument('short_url', type=str)
        self.reqparse.add_argument('public', type=bool)
        self.reqparse.add_argument('privacy', type=bool)
        super(UrlShortenerAPI, self).__init__()

    def get(self, user_id: int, link_id: int):
        link = Link.query.filter_by(user_id=user_id, id=link_id).first()
        if not link:
            raise LinkNotFoundError
        serializer = LinkSerializer()
        return serializer.dump(link)

    def patch(self, user_id: int, link_id: int):
        link = Link.query.filter_by(user_id=user_id, id=link_id).first()
        if not link:
            raise LinkNotFoundError
        data: dict = self.reqparse.parse_args()
        updated_data: dict = data.copy()
        for k, v in data.items():
            if not v:
                updated_data.pop(k)
        if not updated_data:
            raise NoUpdatedDataLinksError
        serializer = LinkSerializer()
        for k, v in updated_data.items():
            setattr(link, k, v)
        try:
            db.session.add(link)
            db.session.commit()
        except IntegrityError:
            raise
        return {'message': 'Data update completed successfully', 'link': serializer.dump(link)}

    def delete(self, user_id: int, link_id: int):
        link = Link.query.filter_by(user_id=user_id, id=link_id).first()
        if not link:
            raise LinkNotFoundError
        serializer = LinkSerializer()
        link_data = serializer.dump(link)
        db.session.delete(link)
        db.session.commit()
        return {'message': f'Link was deleted successfully.', 'link': link_data}, 204


class AuthUrlShortenerCollectionAPI(Resource):
    method_decorators = [jwt_required]

    def get(self, user_id: int):
        links = Link.query.filter(or_(Link.user_id == user_id, Link.public == True)).all()
        serializer = LinkSerializer(many=True)
        return serializer.dump(links)


class PublicUrlShortenerCollectionAPI(Resource):
    method_decorators = [jwt_optional]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('long_url', type=str, required=True, help='Missing long_url parameter')
        self.reqparse.add_argument('short_url', type=str, default=make_short_url())
        self.reqparse.add_argument('public', type=bool, default=True)
        self.reqparse.add_argument('privacy', type=bool, default=False)
        super(PublicUrlShortenerCollectionAPI, self).__init__()

    def get(self):
        links = Link.query.filter_by(public=True)
        serializer = LinkSerializer(many=True)
        return serializer.dump(links)

    def post(self):
        username: str = get_jwt_identity()
        data: dict = self.reqparse.parse_args(http_error_code=400)
        serializer = LinkSerializer()
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
