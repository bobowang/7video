# coding=utf-8

import os

from flask import Flask
from flask_restful import Api

from apps.api import *
from apps.common import *
from apps.home import *


def create_app():
    flask_app = Flask(__name__)

    config_file = './config.py'
    if os.getenv('FLASK_CONFIG_FILE'):
        config_file = os.getenv('FLASK_CONFIG_FILE')

    flask_app.config.from_pyfile(config_file)
    db.init_app(flask_app)
    flask_api = Api(flask_app)

    flask_app.register_blueprint(home_bp, url_prefix='/')
    flask_api.add_resource(ForumListApi, '/api/v1/forums', endpoint='forums')
    flask_api.add_resource(ForumApi, '/api/v1/forums/<int:forum_id>', endpoint='forum')

    return flask_app


__all__ = ["create_app"]
