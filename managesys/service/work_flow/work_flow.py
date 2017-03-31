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
@work_flow.route('/tranctproc/todo',methods=['POST'])
@login_required
def todo_tranctproc():
    '''
    处理流程
    :param :
    :return:
    '''
    user_flow_id = request.form['flow_id']
    result=request.form['result']
    user_flow_info=UserFlowInfo.query.get(user_flow_id)
    flow_step_infos=sorted(user_flow_info.flow_info.flow_step_infos,key=attrgetter('order_no'),reverse=False)
    if  not result=="end":
        user_flow_info.is_finish=True
        return '''
                    <label>终止</label>
            '''
    if user_flow_info.step_id < len(flow_step_infos):
        user_flow_info.step_id=flow_step_infos[user_flow_info.step_id+1].step_id
    return '''
            <label>添加成功</label>
    '''

@work_flow.route('/tranctproc/add',methods=['POST'])
@login_required
def add_tranctproc():
    flow_info_id=request.form['workflow']
    flow_info=FlowInfo.query.get(flow_info_id)
    flow_step_infos=sorted(flow_info.flow_step_infos,key=attrgetter('order_no'),reverse=False)
    user_flow_info=UserFlowInfo()
    user_flow_info.user_id=int(session['user_id'])
    user_flow_info.flow_info_id=int(flow_info_id)
    user_flow_info.step_id=int(flow_step_infos[0].id)
    user_flow_info.next_user_id=flow_step_infos[1].flow_action_info.role.users.first().id
    db.session.add(user_flow_info)
    try:
        db.session.commit()
    except Exception as e:
        print e.message
        db.session.rollback()
    tranct_proc=TranctProc()
    tranct_proc.step_action=1
    tranct_proc.user_flow_info_id=user_flow_info.id
    tranct_proc.desc=request.form['reason']
    db.session.add(tranct_proc)
    try:
        db.session.commit()
    except Exception as e:
        print e.message
        db.session.rollback()
    return '''
        <label>添加成功</label>
    '''
@work_flow.route('/tranctproc',methods=['POST'])
@login_required
def flow_tranct_proc():
    flow_info_id=request.form['workflow']
    user_flow_infos=UserFlowInfo.query.filter_by(flow_info_id=flow_info_id,user_id=session['user_id'],is_finish=False).first()
