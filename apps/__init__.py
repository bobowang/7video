# coding=utf-8

from flask import Flask
from flask_restful import Api

import config
from apps.api import *
from apps.common import *
from apps.home import *


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)
    db.init_app(flask_app)
    flask_api = Api(flask_app)

    flask_app.register_blueprint(home_bp, url_prefix='/')
    flask_api.add_resource(ForumListApi, '/api/v1/forums', endpoint='forums')
    flask_api.add_resource(ForumApi, '/api/v1/forums/<int:forum_id>', endpoint='forum')

    return flask_app


__all__ = ["create_app"]
