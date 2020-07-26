# coding=utf-8

from sqlalchemy.inspection import inspect

from application.utils import db


# 构建Category模型类
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer)
    title = db.Column(db.String())

    def keys(self):
        return inspect(self).attrs.keys()

    def __getitem__(self, key):
        return getattr(self, key)
