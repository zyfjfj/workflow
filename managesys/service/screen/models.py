# coding:utf-8
from flask_admin.contrib.sqla import ModelView
from managesys import db, admin,is_debug
from datetime import datetime

class ClientStatus(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    pic_one = db.Column(db.Integer)
    pic_two= db.Column(db.Integer)
    face= db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __init__(self, pic_one, pic_two,face):
        self.pic_one = pic_one
        self.pic_two = pic_two

    def __repr__(self):
        return '<User %r>' % self.usernam

class ClientStatusView(ModelView):
    # 是否允许创建
    can_create = False
    # 显示的字段
    column_searchable_list = ('pic_one', 'pic_two',"face","create_time")

    def is_accessible(self):
        return is_debug

    def __init__(self, session, **kwargs):
        super(ClientStatusView, self).__init__(ClientStatus, session, **kwargs)

admin.add_view(ClientStatusView(db.session))