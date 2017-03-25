#coding:utf-8

from managesys import db, is_debug, admin
from flask_admin.contrib.sqla import ModelView
from ..work_flow.models import FlowInfo

class Role(db.Model):
    __tablename__="role"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    flow_info=db.relationship("FlowInfo")
    create_time=db.Column(db.DateTime)
    enable=db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Role %r>' % self.name


admin.add_view(ModelView(Role,db.session))
