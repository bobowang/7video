# coding=utf-8

import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api

from apps.api import *
from apps.home import *
from apps.models import *
from .utils import db


def get_config_file():
    return os.getenv('FLASK_CONFIG_FILE') or 'config.py'


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile(get_config_file())

    db.init_app(flask_app)
    flask_app.register_blueprint(home_bp, url_prefix='/')

    flask_api = Api(flask_app)
    flask_api.add_resource(ForumListApi, '/api/v1/forums', endpoint='forums')
    flask_api.add_resource(ForumApi, '/api/v1/forums/<int:forum_id>', endpoint='forum')

    admin = Admin(flask_app, name=flask_app.config['ADMIN_NAME'], template_mode='bootstrap3')
    admin.add_view(ModelView(Actor, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Forum, db.session))

    return flask_app


__all__ = ["create_app"]
