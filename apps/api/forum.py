# coding=utf-8

from flask import Blueprint, current_app, request, jsonify, make_response

from apps.models import *

api_bp = Blueprint('api', __name__)


@api_bp.route('/forums', methods=['GET'])
def get_forums():
    cid = request.args.get('cid', type=int)
    filters = [(Forum.cid == cid)] if cid else []

    forum_pagination = Forum.query.filter(*filters).order_by(Forum.create_time.desc()).paginate(
        page=request.args.get('page', 1, type=int),
        per_page=current_app.config['FORUMS_PER_PAGE'],
        error_out=False)

    pagination = {
        "current_page": forum_pagination.page,
        "pages": forum_pagination.pages,
        "per_page": forum_pagination.per_page,
        "has_prev": forum_pagination.has_prev,
        "has_next": forum_pagination.has_next,
        "total": forum_pagination.total,
    }

    data = [forum.to_dict() for forum in forum_pagination.items]
    return jsonify({'code': 200, 'message': 'success', 'pagination': pagination, 'data': data})


@api_bp.route('/forums/<int:id>', methods=['GET'])
def get_forum(id):
    forum = Forum.query.get(id)
    if not forum:
        return make_response(jsonify({'code': 404, 'message': 'not exist'}), 404)
    return jsonify({'code': 200, 'message': 'success', 'data': forum.to_dict()})
