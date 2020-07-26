# coding=utf-8

from flask_security import UserMixin

from application.utils import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(256))
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(32), default='')
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

    def get_id(self):
        return self.id
