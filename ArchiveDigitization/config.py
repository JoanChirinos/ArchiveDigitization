"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = path.join(basedir, 'static')
    TEMPLATES_FOLDER = path.join(basedir, 'templates')
    UPLOAD_FOLDER = path.join(STATIC_FOLDER, 'imgs/')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = path.join(basedir, environ.get('PROD_DATABASE_URI'))
    #SERVER_NAME = "risleyarchives.com:80"


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = path.join(basedir, environ.get('DEV_DATABASE_URI'))
    # SERVER_NAME = "dev.risarch:5000"

# Source: https://hackersandslackers.com/configure-flask-applications
