# coding=utf-8
import os

from flask import Flask
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_restful import Api
from flask_security import Security
from flask_security.datastore import SQLAlchemyUserDatastore

from application.admin import *
from application.api import *
from application.home import *
from application.models import *
from application.utils import *


def get_config_file():
    return os.getenv('FLASK_CONFIG_FILE') or 'config.py'


def upgrade_database():
    if table_exists('user'):
        return

    db.create_all()
    db.session.commit()

    user_role = Role(name='user', description='用户组')
    administrator_role = Role(name='administrator', description='管理员组')
    db.session.add(user_role)
    db.session.add(administrator_role)
    db.session.commit()
    print("create roles success")

    db.session.add(
        User(username='admin', password=hash_password('admin'), email='admin', roles=[user_role, administrator_role]))
    db.session.commit()
    print("create admin user success")


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile(get_config_file())

    db.init_app(flask_app)
    flask_app.register_blueprint(home_bp, url_prefix='/')

    flask_api = Api(flask_app)
    flask_api.add_resource(ForumListApi, '/api/v1/forums', endpoint='forums')
    flask_api.add_resource(ForumApi, '/api/v1/forums/<int:forum_id>', endpoint='forum')

    flask_admin = Admin(flask_app, name=flask_app.config['ADMIN_NAME'],
                        base_template='admin/my_master.html',
                        template_mode='bootstrap3',
                        index_view=MyAdminIndexView())
    flask_admin.add_view(ActorView(Actor, db.session))
    flask_admin.add_view(CategoryView(Category, db.session))
    flask_admin.add_view(ForumView(Forum, db.session))
    flask_admin.add_view(UserView(User, db.session))
    flask_admin.add_view(RoleView(Role, db.session))

    user_data_store = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(flask_app, datastore=user_data_store)

    @security.context_processor
    def security_context_processor():
        return dict(admin_base_template=flask_admin.base_template,
                    admin_view=flask_admin.index_view,
                    h=admin_helpers, get_url=url_for)

    with flask_app.app_context():
        upgrade_database()

    return flask_app


__all__ = ["create_app"]
