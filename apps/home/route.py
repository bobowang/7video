# coding=utf-8

import datetime
import os

from flask import g, Blueprint, current_app, render_template, flash
from flask_paginate import Pagination
from sqlalchemy.sql import func

from apps.common import *
from apps.models import *

home_bp = Blueprint('home', __name__,
                    static_folder=os.path.join(os.path.dirname(__file__), '../static'),
                    template_folder=os.path.join(os.path.dirname(__file__), '../templates'))


@home_bp.before_request
def home_init():
    g.categories = {}
    for row in Category.query:
        g.categories[row.cid] = row.title
    g.home_title = current_app.config['HOME_TITLE']


@home_bp.route('/')
@home_bp.route('/statistic')
def index():
    flash(u'声明：本站为资讯类网站，我们不提供任何影视的上传、下载、存储、播放，版权归属原电影制作公司，其他问题请邮件bostinwangbo@gmail.com', category='warning')

    today = datetime.date.today()
    today_result = dict()
    for item in db.session.query(Forum.cid, func.count('*')) \
            .filter(Forum.create_date == today) \
            .group_by(Forum.cid).order_by(Forum.cid).all():
        today_result[item[0]] = item[1]

    yesterday = (datetime.date.today() + datetime.timedelta(days=-1))
    yesterday_result = dict()
    for item in db.session.query(Forum.cid, func.count('*')) \
            .filter(Forum.create_date == yesterday) \
            .group_by(Forum.cid).order_by(Forum.cid).all():
        yesterday_result[item[0]] = item[1]

    results = []
    for row in db.session.query(Forum.cid, func.count('*')) \
            .group_by(Forum.cid).order_by(Forum.cid).all():
        cid = row[0]
        record = {'cid': cid,
                  'title': g.categories[cid],
                  'total': row[1],
                  'today': today_result[cid] if cid in today_result else 0,
                  'yesterday': yesterday_result[cid] if cid in yesterday_result else 0
                  }
        results.append(record)

    return render_template('index.html', results=results)


@home_bp.route('/forums/<int:cid>/', defaults={'page': 1})
@home_bp.route('/forums/<int:cid>/<int:page>')
def forums(cid, page):
    filters = [(Forum.cid == cid)] if cid else []
    total = Forum.query.filter(*filters).count()
    per_page = current_app.config['FORUMS_PER_PAGE']

    start = (page - 1) * per_page
    end = page * per_page
    forums = Forum.query.filter(*filters).order_by(Forum.create_time.desc()).slice(start, end)

    pagination = Pagination(bs_version=4,
                            total=total,
                            page=page,
                            per_page=per_page)

    return render_template('forums.html', forums=forums,
                           pagination=pagination,
                           active_url="url-cid-%d" % cid)
