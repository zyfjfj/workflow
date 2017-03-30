#coding:utf-8
from operator import attrgetter

from flask import request,session
from flask_login import login_required

from managesys import db
from flask import Blueprint

from managesys.moudel.util import ok,objs_to_json
from managesys.service.login.models import User
from managesys.service.role.models import Role
from models import FlowInfo, TranctProc, UserFlowInfo, FlowActionInfo

work_flow = Blueprint('work_flow', __name__, url_prefix='/workflow')


@work_flow.route('/')
def index():
    return 'work flow!'

@work_flow.route('/',methods=['GET','POST'])
def flow_infos():
    query = db.session.query(FlowInfo)
    if request.method == "GET":
        flow_infos=query.all()
        if flow_infos:
            return ok(objs_to_json(flow_infos))

@work_flow.route('/<user_name>',methods=['GET','POST'])
@login_required
def flow_infos_by_role(user_name):
    '''
    获取和添加角色拥有的流程
    :param role_name:
    :return:
    '''
    if request.method=="GET":
        users=User.query.filter_by(name=user_name)
        if users:
            roles=users.first().roles.all()
            return ok(objs_to_json(roles))
        return ok(u"没有数据")

@work_flow.route('/tranctproc',methods=['POST'])
@login_required
def flow_tranct_proc():
    flow_info_id=request.form['workflow']
    user_flow_infos=UserFlowInfo.query.filter_by(flow_info_id=flow_info_id,user_id=session['user_id'],is_finish=False).first()
    if user_flow_infos:
        user_flow_info=user_flow_infos
    else:
        flow_info=FlowInfo.query.filter_by(id=flow_info_id).first()
        flow_step_infos=sorted(flow_info.flow_step_infos,key=attrgetter('order_no'),reverse=False)
        user_flow_info=UserFlowInfo()
        user_flow_info.user_id=session['user_id']
        user_flow_info.flow_info_id=flow_info_id
        user_flow_info.step_id=flow_step_infos[0]
        db.session.add(user_flow_info)
        db.session.commit()
    # tranct_proc=TranctProc()
    # tranct_proc.user_id=
    # tranct_proc.flow_info_id=
    # tranct_proc.desc=request.form['reason']
    print request.form