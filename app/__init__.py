"""Creates and configures an application"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from instance.config import app_config


db = SQLAlchemy()


from app.blueprints.auth import auth
from app.exceptions import handler


def create_app(config_name):
    """This will create the application and setup all the 
    other extensions"""

    # initialize flask and jwt
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)

    # load configuration
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # register blueprints
    app.register_blueprint(auth)

    # initialize the database
    db.init_app(app)
    # application exceptions handler
    handler.init_app(app)
    # jwt blacklists handler
    handler.init_jwt(jwt)

    return app
