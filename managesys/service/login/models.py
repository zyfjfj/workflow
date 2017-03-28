#!/usr/bin/python
# coding:utf-8
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

from managesys import db, admin,is_debug
from datetime import datetime
from ..role.models import Role
user_role=db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    roles=db.relationship('Role', secondary=user_role, backref=db.backref('users',lazy='dynamic'), lazy='dynamic')
    email = db.Column(db.String(120), unique=True)
    create_time = db.Column(db.DateTime)


    def __repr__(self):
        return '<User %r>' % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class UserView(ModelView):
    # 是否允许创建
    can_create = is_debug
    # 显示的字段
    column_searchable_list = ('name', 'email')

    def is_accessible(self):
        return is_debug

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)

admin.add_view(UserView(db.session))