#coding:utf-8
import datetime

from managesys import db,is_debug, admin
from flask_admin.contrib.sqla import ModelView

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
    desc=db.Column(db.String(500))
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))
    def __repr__(self):
        return u'<FlowActionInfo {}>'.format(self.name)

class FlowStepInfo(db.Model):
    '''
    流程步骤对应表
    '''
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    flow_info_id=db.Column(db.Integer,db.ForeignKey("flow_info.id"))
    flow_info = db.relationship("FlowInfo",backref=db.backref('flow_step_infos', order_by=id))
    flow_action_info_id=db.Column(db.Integer,db.ForeignKey("flow_action_info.id"))
    flow_action_info=db.relationship("FlowActionInfo",backref=db.backref('flow_step_infos'))
    repeat_no=db.Column(db.Integer,default=1)#重复次数
    order_no=db.Column(db.Integer)           #排序号
    def __repr__(self):
        return u'<FlowStepInfo {}>'.format(self.name)

class UserFlowInfo(db.Model):
    '''
    用户流程表
    '''
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    flow_info_id=db.Column(db.Integer,db.ForeignKey("flow_info.id"))
    flow_info=db.relationship('FlowInfo',backref=db.backref('user_flow_infos'))
    step_id=db.Column(db.Integer,db.ForeignKey("flow_step_info.id"))
    step=db.relationship('FlowStepInfo',backref=db.backref('user_flow_infos'))
    next_user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    is_finish=db.Column(db.Boolean,default=False)
    create_time=db.Column(db.DateTime,default=datetime.datetime.now())

    def __repr__(self):
        return u'<UserFlowInfo {}>'.format(self.id)
class TranctProc(db.Model):
    '''
    用户流程表详尽
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_flow_info_id=db.Column(db.Integer,db.ForeignKey("user_flow_info.id"))
    user_flow_info=db.relationship('UserFlowInfo',backref=db.backref('tranct_procs', lazy='dynamic'))
    step_action=db.Column(db.Integer)#同意1，退回2，终止3
    step_time=db.Column(db.DateTime,default=datetime.datetime.now())
    desc=db.Column(db.String(500))

    def __repr__(self):
        return u'<TranctProc {}>'.format(self.id)
class FlowView(ModelView):
    # 是否允许创建
    can_create = True

    def is_accessible(self):
        return is_debug


admin.add_view(FlowView(FlowInfo,db.session))
admin.add_view(FlowView(FlowStepInfo,db.session))
admin.add_view(FlowView(FlowActionInfo,db.session))
admin.add_view(ModelView(TranctProc,db.session))