#coding:utf-8
import datetime

from managesys import db,is_debug, admin
from flask_admin.contrib.sqla import ModelView
from ..role.models import Role

#role和flowinfo是多对多关系
role_flow = db.Table('role_flow',
    db.Column('flow_info_id', db.Integer, db.ForeignKey('flow_info.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class FlowInfo(db.Model):
    '''
    流程信息表
    '''
    __tablename__="flow_info"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    desc=db.Column(db.String(500))
    create_time=db.Column(db.DateTime,default=datetime.datetime.now())
    enable=db.Column(db.Boolean,default="Y")

    def __repr__(self):
        return u'<FlowInfo {}>'.format(self.name)

class FlowActionInfo(db.Model):
    '''
    步骤信息表
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    role_id=db.column(db.Integer,db.ForeignKey("role.id"))
    role = db.relationship("Role",backref='flow_action_infos', lazy='dynamic')
    desc=db.Column(db.String(500))

    def __repr__(self):
        return u'<FlowActionInfo {}>'.format(self.name)

class FlowStepInfo(db.Model):
    '''
    流程步骤对应表
    '''
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    flow_info=db.Column(db.Integer,db.ForeignKey("flow_info.id"))
    flow_infos = db.relationship("FlowInfo",backref=db.backref('flow_step_infos', order_by=id))
    flow_action_info=db.Column(db.Integer,db.ForeignKey("flow_action_info.id"))
    flow_action_infos=db.relationship("FlowActionInfo")
    repeat_no=db.Column(db.Integer,default=1)#重复次数
    order_no=db.Column(db.Integer)           #排序号
    def __repr__(self):
        return u'<FlowStepInfo {}>'.format(self.name)

class UserFlowInfo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    flow_info_id=db.Column(db.Integer,db.ForeignKey("flow_info.id"))
    step_id=db.Column(db.Integer,db.ForeignKey("flow_step_info.id"))
    next_user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    is_finish=db.Column(db.Boolean,default="N")

class TranctProc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_flow_info_id=db.Column(db.Integer,db.ForeignKey("user_flow_info.id"))
    user_flow_info=db.relationship('UserFlowInfo',backref=db.backref('tranct_procs', lazy='dynamic'))
    step_action=db.Column(db.Integer)
    step_time=db.Column(db.DateTime,default=datetime.datetime.now())
    desc=db.Column(db.String(500))

class FlowView(ModelView):
    # 是否允许创建
    can_create = True

    def is_accessible(self):
        return is_debug


admin.add_view(FlowView(FlowInfo,db.session))
admin.add_view(FlowView(FlowStepInfo,db.session))
admin.add_view(FlowView(FlowActionInfo,db.session))
admin.add_view(ModelView(TranctProc,db.session))