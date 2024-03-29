# coding=utf-8

import datetime
import os

from flask import g, Blueprint, current_app, render_template, flash
from flask import request, redirect, url_for, jsonify
from flask_paginate import Pagination
from sqlalchemy.sql import func, desc

from application.models import *
from application.utils import db

home_bp = Blueprint('home', __name__,
                    static_folder=os.path.join(os.path.dirname(__file__), '../static'),
                    template_folder=os.path.join(os.path.dirname(__file__), '../templates'))


@home_bp.before_request
def home_init():
    g.categories = {}
    for row in Category.query.order_by(Category.cid):
        g.categories[row.cid] = row.title
    g.home_title = current_app.config['HOME_TITLE']
    g.per_page = current_app.config['FORUMS_PER_PAGE']


@home_bp.route('/')
def index():
    flash(u'声明：本站为资讯类网站，我们不提供任何影视的上传、下载、存储、播放，版权归属原电影制作公司', category='warning')

    today = datetime.date.today()
    today_result = dict()
    for item in db.session.query(Forum.cid, func.count('*')) \
            .filter(Forum.create_date == today) \
            .group_by(Forum.cid).all():
        today_result[item[0]] = item[1]

    yesterday = (datetime.date.today() + datetime.timedelta(days=-1))
    yesterday_result = dict()
    for item in db.session.query(Forum.cid, func.count('*')) \
            .filter(Forum.create_date == yesterday) \
            .group_by(Forum.cid).all():
        yesterday_result[item[0]] = item[1]

    results = []
    for row in db.session.query(Forum.cid, func.count('*')) \
            .group_by(Forum.cid).all():
        cid = row[0]
        record = {'cid': cid,
                  'title': g.categories[cid],
                  'total': row[1],
                  'today': today_result[cid] if cid in today_result else 0,
                  'yesterday': yesterday_result[cid] if cid in yesterday_result else 0
                  }
        results.append(record)

    return render_template('home/index.html', results=results)


@home_bp.route('/top')
def top():
    page = request.args.get('page', default=1, type=int)

    total = db.session.query(Forum.actor_pro, func.count('*').label('cnt')) \
        .group_by(Forum.actor_pro).order_by(desc('cnt')).count()

    start = (page - 1) * g.per_page
    end = page * g.per_page

    data = db.session.query(Forum.actor_pro, func.count('*').label('cnt')) \
        .group_by(Forum.actor_pro).order_by(desc('cnt')).slice(start, end)

    pagination = Pagination(bs_version=4,
                            total=total,
                            page=page,
                            per_page=g.per_page)

    return render_template('home/top.html', data=data,
                           pagination=pagination,
                           active_url="url-cid-top")


@home_bp.route('/forums/<int:cid>/')
def forums(cid):
    filters = [(Forum.cid == cid)] if cid else []
    total = Forum.query.filter(*filters).count()

    page = request.args.get('page', default=1, type=int)
    start = (page - 1) * g.per_page
    end = page * g.per_page
    data = Forum.query.filter(*filters).order_by(Forum.fid.desc(), Forum.id.desc()).slice(start, end)

    pagination = Pagination(bs_version=4,
                            total=total,
                            page=page,
                            per_page=g.per_page)

    return render_template('home/forums.html', forums=data,
                           pagination=pagination,
                           active_url="url-cid-%d" % cid)


@home_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword').strip()
        return redirect(url_for('home.search', keyword=keyword))

    page = request.args.get('page', default=1, type=int)

    filters = []
    actor_pro = request.args.get('actor_pro')
    filters.append((Forum.actor_pro == actor_pro)) if actor_pro else None
    actor = request.args.get('actor')
    filters.append((Forum.actor == actor)) if actor else None
    keyword = request.args.get('keyword')
    filters.append((Forum.title.like('%' + keyword + '%'))) if keyword else None
    total = Forum.query.filter(*filters).count()

    start = (page - 1) * g.per_page
    end = page * g.per_page
    data = Forum.query.filter(*filters).order_by(Forum.fid.desc()).slice(start, end)

    pagination = Pagination(bs_version=4,
                            total=total,
                            page=page,
                            per_page=g.per_page)

    return render_template('home/forums.html', forums=data,
                           pagination=pagination)


@home_bp.route('/modify_actor')
def modify_actor():
    result = []
    for actor in Actor.query.filter(Actor.need_modify == 1).order_by(Actor.id.desc()).all():
        actor_old = actor['actor'].strip()
        actor_new = actor['actor_pro'].strip()

        ret = db.session.query(Forum).filter(Forum.cid in (103, 36, 37)) \
            .filter(Forum.actor_pro in ('未知', '素人')) \
            .filter(Forum.title.like('%' + actor_new + '%')) \
            .update({'actor_pro': actor_new}, synchronize_session=False)
        db.session.commit()
        if ret > 0:
            result.append("search %s, %d modified" % (actor_new, ret))

        if actor_old != actor_new:
            ret = db.session.query(Forum).filter(Forum.cid in (103, 36, 37)) \
                .filter(Forum.actor_pro == actor_old) \
                .update({'actor_pro': actor_new}, synchronize_session=False)
            db.session.commit()
            if ret > 0:
                result.append("%s => %s, %d modified" % (actor_old, actor_new, ret))

    return jsonify(result)

def pic_url_for(url):
    if url.startswith("http"):
        return url
    return "https://www.sehuatang.org/" + url
