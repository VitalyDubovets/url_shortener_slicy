import dotenv
import os


basedir = os.path.abspath(os.path.dirname(__file__))

# Read .env file from project's root
dotenv.load_dotenv(dotenv_path=os.path.join(basedir, '.env'), override=True)


class Config:
    CSRF_ENABLED = True
    DEBUG = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    REDIS_DB = 0
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    SECRET_KEY = os.getenv('SECRET_KEY') or 'nice secret key'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}' \
                              f'@{os.getenv("DATABASE_HOST")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
