# coding=utf-8

from flask_security import RoleMixin

from application.utils import db


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))

    def __str__(self):
        return self.name
