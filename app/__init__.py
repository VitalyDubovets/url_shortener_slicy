import dotenv
import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_redis import Redis
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import basedir


dotenv.load_dotenv(dotenv_path=os.path.join(basedir, '.env'), override=True)

api = Api(prefix='/api/v1')
auth = HTTPBasicAuth()
db = SQLAlchemy()
redis = Redis()


def load_models():
    from app.links import models as links_models
    from app.users import models as users_models


load_models()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_CONFIG'))

    db.init_app(app)
    redis.init_app(app)
    api.init_app(app)

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from .links import links as links_blueprint
    app.register_blueprint(links_blueprint)

    return app
