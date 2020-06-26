# coding=utf-8

import datetime
import os

from flask import g, Blueprint, current_app, render_template, flash
from flask import request, redirect, url_for, jsonify
from flask_paginate import Pagination
from sqlalchemy.sql import func, desc

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
    g.per_page = current_app.config['FORUMS_PER_PAGE']


@home_bp.route('/')
def index():
    flash(u'声明：本站为资讯类网站，我们不提供任何影视的上传、下载、存储、播放，版权归属原电影制作公司', category='warning')

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


@home_bp.route('/top')
def top():
    page = request.args.get('page', default=1, type=int)

    total = db.session.query(Forum.actor_pro, func.count('*').label('cnt')) \
        .filter(Forum.actor_pro != u'未知') \
        .group_by(Forum.actor_pro).order_by(desc('cnt')).count()

    start = (page - 1) * g.per_page
    end = page * g.per_page

    data = db.session.query(Forum.actor_pro, func.count('*').label('cnt')) \
        .group_by(Forum.actor_pro).order_by(desc('cnt')).slice(start, end)

    pagination = Pagination(bs_version=4,
                            total=total,
                            page=page,
                            per_page=g.per_page)

    return render_template('top.html', data=data,
                           pagination=pagination,
                           active_url="url-cid-top")


@home_bp.route('/forums/<int:cid>/')
def forums(cid):
    filters = [(Forum.cid == cid)] if cid else []
    total = Forum.query.filter(*filters).count()

    page = request.args.get('page', default=1, type=int)
    start = (page - 1) * g.per_page
    end = page * g.per_page
    forums = Forum.query.filter(*filters).order_by(Forum.create_time.desc()).slice(start, end)

    pagination = Pagination(bs_version=4,
                            total=total,
                            page=page,
                            per_page=g.per_page)

    return render_template('forums.html', forums=forums,
                           pagination=pagination,
                           active_url="url-cid-%d" % cid)


@home_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
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
    forums = Forum.query.filter(*filters).order_by(Forum.create_time.desc()).slice(start, end)

    pagination = Pagination(bs_version=4,
                            total=total,
                            page=page,
                            per_page=g.per_page)

    return render_template('forums.html', forums=forums,
                           pagination=pagination)


@home_bp.route('/tools')
def tools():
    return render_template('tools.html')


@home_bp.route('/modify_actor')
def modify_actor():
    result = []
    for actor in Actor.query.filter(Actor.need_modify == 1).all():
        actor_old = actor['actor'].strip()
        actor_new = actor['actor_pro'].strip()
        if actor_old != actor_new:
            ret = db.session.query(Forum) \
                .filter(Forum.actor_pro == actor_old) \
                .update({'actor_pro': actor_new}, synchronize_session=False)
            db.session.commit()
            if ret > 0:
                result.append("%s => %s, %d modified" % (actor_old, actor_new, ret))

        ret_keyword = db.session.query(Forum) \
            .filter(Forum.actor_pro != actor_new) \
            .filter(Forum.title.like('%' + actor_new + '%')) \
            .update({'actor_pro': actor_new}, synchronize_session=False)
        db.session.commit()
        if ret_keyword > 0:
            result.append("search %s, %d modified" % (actor_new, ret_keyword))
            item = db.session.query(Forum) \
                .filter(Forum.actor_pro != actor_new) \
                .filter(Forum.title.like('%' + actor_new + '%')).count()
            print(ret_keyword, item)

    return jsonify(result)


@home_bp.route('/replace_actor_pro', methods=['POST'])
def replace_actor_pro():
    actor_pro_old = request.form.get('actor_pro_old').strip()
    actor_pro_new = request.form.get('actor_pro_new').strip()

    if not actor_pro_old:
        flash(u'原演员不能为空', category='warning')
        return render_template('tools.html')
    if not actor_pro_new:
        flash(u'新演员不能为空', category='warning')
        return render_template('tools.html')
    if actor_pro_old == actor_pro_new:
        flash(u'演员修改前后不能相同', category='warning')
        return render_template('tools.html')

    ret = db.session.query(Forum) \
        .filter(Forum.actor_pro == actor_pro_old) \
        .update({'actor_pro': actor_pro_new}, synchronize_session=False)
    db.session.commit()

    flash(u'修改成功:%d条，%s=>%s' % (ret, actor_pro_old, actor_pro_new), category='info')
    return render_template('tools.html')


@home_bp.route('/modify_actor_pro_keyword', methods=['POST'])
def modify_actor_pro_keyword():
    keyword = request.form.get('keyword').strip()
    actor_pro_new = request.form.get('actor_pro_new').strip()

    if not keyword:
        flash(u'关键字不能为空', category='warning')
        return render_template('tools.html')
    if not actor_pro_new:
        flash(u'新演员不能为空', category='warning')
        return render_template('tools.html')

    ret = db.session.query(Forum) \
        .filter(Forum.actor_pro != actor_pro_new) \
        .filter(Forum.title.like('%' + keyword + '%')) \
        .update({'actor_pro': actor_pro_new}, synchronize_session=False)
    db.session.commit()

    flash(u'修改成功:%d条，%s ~ %s' % (ret, keyword, actor_pro_new), category='info')
    return render_template('tools.html')
