# coding:utf-8
import datetime

from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

from managesys import db, is_debug, admin

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                     )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return u'<user {}>'.format(self.name)


class UserView(ModelView):
    # 是否允许创建
    can_create = is_debug
    # 显示的字段
    column_searchable_list = ('name', 'email')

    def is_accessible(self):
        return is_debug

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


# role和flowinfo是多对多关系
role_flow = db.Table('role_flow',
                     db.Column('flow_info_id', db.Integer, db.ForeignKey('flow_info.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                     )


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    flow_infos = db.relationship('FlowInfo', secondary=role_flow, backref=db.backref('role', lazy='dynamic'),
                                 lazy='dynamic')
    flow_action_infos = db.relationship("FlowActionInfo", backref=db.backref("role"))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    enable = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return u'<角色 {}>'.format(self.name)


class FlowInfo(db.Model):
    '''
    流程信息表
    '''
    __tablename__ = "flow_info"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    desc = db.Column(db.String(500))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    enable = db.Column(db.Boolean, default="Y")

    def __repr__(self):
        return u'<FlowInfo {}>'.format(self.name)


class FlowActionInfo(db.Model):
    '''
    步骤信息表
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    desc = db.Column(db.String(500))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

    def __repr__(self):
        return u'<FlowActionInfo {}>'.format(self.name)


class FlowStepInfo(db.Model):
    '''
    流程步骤对应表
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    flow_info_id = db.Column(db.Integer, db.ForeignKey("flow_info.id"))
    flow_info = db.relationship("FlowInfo", backref=db.backref('flow_step_infos', order_by=id))
    flow_action_info_id = db.Column(db.Integer, db.ForeignKey("flow_action_info.id"))
    flow_action_info = db.relationship("FlowActionInfo", backref=db.backref('flow_step_infos'))
    repeat_no = db.Column(db.Integer, default=1)  # 重复次数
    order_no = db.Column(db.Integer)  # 排序号

    def __repr__(self):
        return u'<FlowStepInfo {}>'.format(self.name)


class UserFlowInfo(db.Model):
    '''
    用户流程表
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    #因为这里有两个user.id，所有要指定改UserFlowInfo.user_id
    user=db.relationship('User',  foreign_keys='UserFlowInfo.user_id',backref=db.backref('user_flow_infos'))
    flow_info_id = db.Column(db.Integer, db.ForeignKey("flow_info.id"))
    flow_info = db.relationship('FlowInfo', backref=db.backref('user_flow_infos'))
    step_id = db.Column(db.Integer, db.ForeignKey("flow_step_info.id"))
    step = db.relationship('FlowStepInfo', backref=db.backref('user_flow_infos'))
    next_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    #因为这里有两个user.id，所有要指定改UserFlowInfo.next_user_id
    next_user=db.relationship('User',  foreign_keys='UserFlowInfo.next_user_id')
    is_finish = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return u'<UserFlowInfo {}>'.format(self.id)


class TranctProc(db.Model):
    '''
    用户流程表详尽
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_flow_info_id = db.Column(db.Integer, db.ForeignKey("user_flow_info.id"))
    user_flow_info = db.relationship('UserFlowInfo', backref=db.backref('tranct_procs', lazy='dynamic'))
    step_action = db.Column(db.Integer)  # 同意1，退回2，终止3
    step_time = db.Column(db.DateTime, default=datetime.datetime.now())
    desc = db.Column(db.String(500))

    def __repr__(self):
        return u'<TranctProc {}>'.format(self.id)


class FlowView(ModelView):
    # 是否允许创建
    can_create = True

    def is_accessible(self):
        return is_debug




admin.add_view(UserView(db.session))
admin.add_view(FlowView(FlowInfo, db.session))
admin.add_view(FlowView(FlowStepInfo, db.session))
admin.add_view(FlowView(FlowActionInfo, db.session))
admin.add_view(ModelView(TranctProc, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(UserFlowInfo, db.session))
