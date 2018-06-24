"""Creates and configures an application"""


from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from instance.config import app_config


db = SQLAlchemy()


from app.blueprints.auth import auth
from app.exceptions import handler
from app.resources.meals import MealResource, MealListResource
from app.resources.menu import MenuResource, MenuListResource
from app.resources.menu_items import MenuItemResource, MenuItemListResource
#from app.resources.notifications import NotificationResource, NotificationListResource


def create_app(config_name):
    """This will create the application and setup all the 
    other extensions"""

    # initialize flask and jwt
    app = Flask(__name__, instance_relative_config=True)
    # load configuration
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    jwt = JWTManager(app)
    api = Api(app, prefix='/api/v1')

    # register endpoints
    app.register_blueprint(auth)
    api.add_resource(MealResource, '/meals/<int:meal_id>')
    api.add_resource(MealListResource, '/meals')
    api.add_resource(MenuResource, '/menus/<int:menu_id>')
    api.add_resource(MenuListResource, '/menus')
    api.add_resource(MenuItemResource, '/menu-items/<int:menu_item_id>')
    api.add_resource(MenuItemListResource, '/menu-items')

    # initialize the database
    db.init_app(app)
    # application exceptions handler
    handler.init_app(app)
    # jwt blacklists handler
    handler.init_jwt(jwt)

    return app
