#coding:utf-8
import datetime

from managesys import db,is_debug, admin
from flask_admin.contrib.sqla import ModelView

class FlowInfo(db.Model):
    '''
    流程信息表
    '''
    __tablename__="flow_info"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    role=db.Column(db.Integer,db.ForeignKey("role.id"))
    create_time=db.Column(db.DateTime,default=datetime.datetime.now())
    enable=db.Column(db.Boolean,default="Y")

    def __repr__(self):
        return u'<FlowInfo {0}>'.format(self.name)

class FlowActionInfo(db.Model):
    '''
    步骤信息表
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return u'<FlowActionInfo {0}>'.format(self.name)
class FlowStepInfo(db.Model):
    '''
    流程步骤对应表
    '''
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    flow_info=db.Column(db.Integer,db.ForeignKey("flow_info.id"))
    flow_action_info=db.Column(db.Integer,db.ForeignKey("flow_action_info.id"))
    repeat_no=db.Column(db.Integer,default=1)#重复次数
    order_no=db.Column(db.Integer)           #排序号
    def __repr__(self):
        return u'<FlowStepInfo {0}>'.format(self.name)
class FlowView(ModelView):
    # 是否允许创建
    can_create = True

    def is_accessible(self):
        return is_debug


admin.add_view(FlowView(FlowInfo,db.session))
admin.add_view(FlowView(FlowStepInfo,db.session))
admin.add_view(FlowView(FlowActionInfo,db.session))