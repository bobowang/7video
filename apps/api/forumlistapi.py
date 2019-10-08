# coding=utf-8

from flask import request, current_app
from flask_restful import Resource, reqparse
from werkzeug.exceptions import HTTPException

from apps.common import *
from apps.models import *


class ForumListApi(Resource):
    def __init__(self):
        self._rp = reqparse.RequestParser(bundle_errors=True)
        self._rp.add_argument('cid', type=int, required=True, location='json')
        self._rp.add_argument('tag', type=unicode, default=u"未知", location='json')
        self._rp.add_argument('url', type=str, required=True, location='json')
        self._rp.add_argument('sn', type=unicode, required=True, location='json')
        self._rp.add_argument('title', type=unicode, required=True, location='json')
        self._rp.add_argument('actor', type=unicode, default=u"未知", location='json')
        self._rp.add_argument('magnet', type=unicode, required=True, location='json')
        self._rp.add_argument('pics', type=str, default="", location='json')
        self._rp.add_argument('create_date', type=str, required=True, location='json')
        self._rp.add_argument('create_time', type=str, required=True, location='json')
        super(ForumListApi, self).__init__()

    def get(self):
        cid = request.args.get('cid', type=int)
        page = request.args.get('page', default=1, type=int)
        filters = [(Forum.cid == cid)] if cid else []

        forum_pagination = Forum.query.filter(*filters).order_by(Forum.create_time.desc()).paginate(
            page=page, per_page=current_app.config['FORUMS_PER_PAGE'], error_out=False)

        pagination = {
            "current_page": forum_pagination.page,
            "pages": forum_pagination.pages,
            "per_page": forum_pagination.per_page,
            "has_prev": forum_pagination.has_prev,
            "has_next": forum_pagination.has_next,
            "total": forum_pagination.total,
        }

        data = [forum.to_dict() for forum in forum_pagination.items]
        return {'code': 200, 'message': 'success', 'pagination': pagination, 'data': data}

    def post(self):
        try:
            args = self._rp.parse_args()
            forum = Forum(args)
            db.session.add(forum)
            db.session.commit()
            return {'code': 201, 'message': 'success', 'data': forum.to_dict()}, 201
        except HTTPException as e:
            return {'code': 400, 'message': e.data['message'], 'data': None}, 400
