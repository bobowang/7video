# coding=utf-8

from sqlalchemy.inspection import inspect

from application.utils import db


# 构建Actor模型类
class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor = db.Column(db.String)
    actor_pro = db.Column(db.String)
    pic = db.Column(db.String)
    need_modify = db.Column(db.Boolean(), default=True)

    def keys(self):
        return inspect(self).attrs.keys()

    def __getitem__(self, key):
        return getattr(self, key)
