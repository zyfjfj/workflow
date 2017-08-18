# -*- coding:utf-8 -*-  
"""
@version: ??
@author: zhayufeng
@describe:新的工作流表
@contact: zyfjfj@163.com
@software: PyCharm
@file: work_flow_models
@time: 2017/8/10 10:48
"""
import datetime
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import Integer, String, Column, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from managesys import db, admin
from ..moudel.util import generate_uuid
from .models import User, Role

Base = db.Model

role_Workflow = db.Table('role_workflow',
                         Column('Workflow_id', ForeignKey('workflow.id'), primary_key=True),
                         Column('role_id', ForeignKey('role.id'), primary_key=True)
                         )


class WorkflowComment(object):
    Agree = 1
    Refuse = 2
    Abort = 3


class Workflow(Base):
    '''
    流程信息表
    '''
    __tablename__ = "workflow"
    id = Column(String(32), primary_key=True, default=generate_uuid)
    name = Column(String(20))
    desc = Column(db.String(500))
    create_time = Column(DateTime, default=datetime.datetime.now())
    roles = relationship("Role", secondary=role_Workflow, backref='workflows')
    enable = Column(Boolean, default="Y")

    def __repr__(self):
        return u'<流程表 {}>'.format(self.name)


class WorkflowStep(Base):
    '''
    步骤表
    '''
    __tablename__ = "workflow_step"
    id = Column(String(32), primary_key=True, default=generate_uuid)
    name = Column(String(20))
    desc = Column(String(500))
    workflow_id = Column(ForeignKey("workflow.id"))
    workflow = relationship("Workflow", backref='WorkflowSteps')
    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship("Role")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    order_no = Column(Integer)  # 排序号
    pre_step_id = Column(ForeignKey("workflow_step.id"))
    pre_step = relationship('WorkflowStep', foreign_keys='WorkflowStep.pre_step_id')
    next_step_id = Column(ForeignKey("workflow_step.id"))
    next_step = relationship('WorkflowStep', foreign_keys='WorkflowStep.next_step_id')

    def get_role(self):
        obj = db.session.query(Role).get(self.role_id)
        return obj

    def __repr__(self):
        return u'<步骤表 {}>'.format(self.name)


class UserWorkflowInfo(Base):
    '''
    用户流程表,记录用户在使用流程
    '''
    id = Column(String(32), primary_key=True, default=generate_uuid)
    # 创建用户
    user_id = Column(ForeignKey("user.id"))
    user = relationship('User', foreign_keys='UserWorkflowInfo.user_id', backref='user_workflow_infos')
    role_id = Column(ForeignKey("role.id"))
    role = relationship('Role', foreign_keys='UserWorkflowInfo.role_id')
    workflow_id = Column(ForeignKey("workflow.id"))
    u_workflow_info = relationship('Workflow', backref='user_workflow_infos')
    # 当前步骤
    step_id = Column(ForeignKey("workflow_step.id"))
    step = relationship('WorkflowStep')
    next_user_id = Column(ForeignKey("user.id"))
    next_user = relationship('User', foreign_keys='UserWorkflowInfo.next_user_id')
    next_role_id = Column(ForeignKey("role.id"))
    next_role = relationship('Role', foreign_keys='UserWorkflowInfo.next_role_id')
    is_finish = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.datetime.now())

    def get_next_user(self):
        obj = db.session.query(User).get(self.next_user_id)
        return obj

    def __repr__(self):
        return u'<用户流程记录表 {},{}>'.format(self.workflow.name, self.step.name)


class UserWorkflowInfoDetail(Base):
    id = Column(String(32), primary_key=True, default=generate_uuid)
    user_workflow_info_id = Column(ForeignKey("user_workflow_info.id"))
    user_workflow_info = relationship('UserWorkflowInfo', backref='details')
    comment = Column(Integer)  # 同意1，退回2，终止3
    step_time = Column(DateTime, default=datetime.datetime.now())
    desc = Column(String(500))

    def __repr__(self):
        return u'<用户处理流程详细表 {}>'.format(self.user_workflow_info)


admin.add_view(ModelView(Workflow, db.session))
admin.add_view(ModelView(WorkflowStep, db.session))
admin.add_view(ModelView(UserWorkflowInfo, db.session))
