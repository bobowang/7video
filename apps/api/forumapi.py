# coding=utf-8

from flask_restful import Resource

from apps.models import *
from apps.utils import db


class ForumApi(Resource):

    def get(self, forum_id):
        forum = Forum.query.get(forum_id)
        if not forum:
            return {'code': 404, 'message': "Forum {} doesn't exist".format(forum_id)}, 404
        return {'code': 200, 'message': 'success', 'data': forum.to_dict()}, 200

    def delete(self, forum_id):
        forum = Forum.query.get(forum_id)
        if not forum:
            return {'code': 404, 'message': "Forum {} doesn't exist".format(forum_id)}, 404
        db.session.delete(forum)
        db.session.commit()
        return {'code': 200, 'message': 'success', 'data': forum.to_dict()}, 200
