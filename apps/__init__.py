# coding=utf-8

import os

from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_restful import Api

from apps.admin import *
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

    admin = Admin(flask_app, name=flask_app.config['ADMIN_NAME'],
                  template_mode='bootstrap3',
                  index_view=AdminIndexView(name='后台首页', menu_icon_type='glyph', menu_icon_value='glyphicon-home'))
    admin.add_view(ActorView(Actor, db.session, name='主演',
                             menu_icon_type='glyph', menu_icon_value='glyphicon-user'))
    admin.add_view(CategoryView(Category, db.session, name='分类',
                                menu_icon_type='glyph', menu_icon_value='glyphicon-tags'))
    admin.add_view(ForumView(Forum, db.session, name='帖子',
                             menu_icon_type='glyph', menu_icon_value='glyphicon-film'))

    return flask_app


__all__ = ["create_app"]
