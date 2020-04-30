from flask_restful import Resource


class UserCollectionAPI(Resource):
    def get(self):
        return {'msg': 'Hello World'}

    def post(self):
        pass


class UserAPI(Resource):
    def get(self, user_id):
        pass

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass
