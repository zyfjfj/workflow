#coding:utf-8
import datetime

from managesys import db, is_debug, admin
from flask_admin.contrib.sqla import ModelView
from ..work_flow.models import FlowInfo,role_flow

class Role(db.Model):
    __tablename__="role"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    flow_infos=db.relationship('FlowInfo', secondary=role_flow, backref=db.backref('role',lazy='dynamic'), lazy='dynamic')
    create_time=db.Column(db.DateTime,default=datetime.datetime.now())
    enable=db.Column(db.Boolean,default=True)

    def __repr__(self):
        return u'<角色 {}>'.format(self.name)


admin.add_view(ModelView(Role,db.session))
