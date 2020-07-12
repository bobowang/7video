# coding=utf-8

import json

from sqlalchemy.inspection import inspect

from apps.common import *


# 构建Forum模型类
class Forum(db.Model):
    __table__name = 'forum'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer)
    tag = db.Column(db.String)
    url = db.Column(db.String, unique=True)
    sn = db.Column(db.String)
    title = db.Column(db.String)
    actor = db.Column(db.String)
    actor_pro = db.Column(db.String)
    magnet = db.Column(db.String)
    pics = db.Column(db.String)
    create_date = db.Column(db.String)
    create_time = db.Column(db.String)
    fid = db.Column(db.Integer)

    def __init__(self, entries):
        self.__dict__.update(entries)

    def keys(self):
        return inspect(self).attrs.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def get_pics(self):
        if self.pics:
            return json.loads(self.pics)
        return None

    def to_dict(self):
        data = dict(self)
        data['pics'] = self.get_pics()
        return data
