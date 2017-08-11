# coding:utf-8
from operator import attrgetter

import flask_login
from flask import Blueprint
from flask import request, session, redirect, url_for, render_template
from flask_login import login_required
from ... import db
from ...model.models import User, FlowInfo, TranctProc, UserFlowInfo, Role
from ...moudel.util import ok, objs_to_json, ObjectToDictEx, err
from ...model.work_flow_models import Workflow, WorkflowStep

work_flow = Blueprint('work_flow', __name__, url_prefix='/workflow')

handling_suggestion = {1: "同意", 2: "不同意", 3: "终止"}


@work_flow.route('/', methods=['GET', 'POST'])
def flow_infos():
    '''
    获取和定义工作流
    :return: 
    '''
    query = db.session.query(FlowInfo)
    if request.method == "GET":
        flow_infos = query.all()
        if flow_infos:
            return render_template('workflow.html', flows=flow_infos)
    else:
        return render_template('workflow.html')


@work_flow.route("/design", methods=['GET'])
def design_workflow():
    return render_template('workflowUi.html')


@work_flow.route('/<user_name>', methods=['GET', 'POST'])
@login_required
def flow_infos_by_role(user_name):
    '''
    获取和添加角色拥有的流程
    :param role_name:
    :return:
    '''
    if request.method == "GET":
        users = User.query.filter_by(name=user_name)
        if users:
            roles = users.first().roles.all()
            return ok(objs_to_json(roles))
        return ok(u"没有数据")


@work_flow.route('/tranctproc/todo', methods=['POST'])
@login_required
def todo_tranctproc():
    '''
    处理流程
    :param :
    :return:
    '''
    user_flow_id = request.form['flow_id']
    result = request.form['result']
    countersign = request.form['countersign']
    user_flow_info = UserFlowInfo.query.get(user_flow_id)
    flow_step_infos = sorted(
        user_flow_info.flow_info.flow_step_infos, key=attrgetter('order_no'), reverse=False)
    if result == "3":
        user_flow_info.is_finish = True
        return '''
                    <label>终止</label>
            '''
    if user_flow_info.step.order_no < len(flow_step_infos) - 1:
        user_flow_info.step = flow_step_infos[user_flow_info.step.order_no + 1]
        user_flow_info.flow_action_info = user_flow_info.step.flow_action_info

        if flow_step_infos[user_flow_info.step.order_no + 1].name != u"结束":
            user_flow_info.next_user_id = flow_step_infos[
                user_flow_info.step.order_no + 1].flow_action_info.role.users.first().id
        else:
            user_flow_info.is_finish = True
    tranct_proc = TranctProc()
    tranct_proc.step_action = int(result)
    tranct_proc.user_flow_info_id = user_flow_info.id
    tranct_proc.desc = countersign
    db.session.add(tranct_proc)
    try:
        db.session.commit()
    except Exception as e:
        print(e.message)
        db.session.rollback()
        return '''
               <label>添加失败</label>
               '''
    return redirect(url_for('index'))
    return '''
            <label>添加成功</label>
    '''


@work_flow.route('/tranctproc/add', methods=['POST'])
@login_required
def add_tranctproc():
    flow_info_id = request.form['workflow']
    flow_info = FlowInfo.query.get(flow_info_id)
    flow_step_infos = sorted(flow_info.flow_step_infos,
                             key=attrgetter('order_no'), reverse=False)
    user_flow_info = UserFlowInfo()
    user_flow_info.user_id = int(session['user_id'])
    user_flow_info.flow_info = flow_info
    user_flow_info.step = flow_step_infos[0]
    user_flow_info.next_user_id = flow_step_infos[1].flow_action_info.role.users.first().id
    db.session.add(user_flow_info)
    try:
        db.session.commit()
    except Exception as e:
        print(e.message)
        db.session.rollback()
    tranct_proc = TranctProc()
    tranct_proc.step_action = 1
    tranct_proc.user_flow_info_id = user_flow_info.id
    tranct_proc.desc = request.form['reason']
    db.session.add(tranct_proc)
    try:
        db.session.commit()
    except Exception as e:
        print(e.message)
        db.session.rollback()
        return
        '''
        <label>添加失败</label>
        '''
    return redirect(url_for('index'))


@work_flow.route('/tranctproc/<user_flow_id>', methods=['GET'])
@login_required
def flow_tranct_proc(user_flow_id):
    pros = TranctProc.query.filter_by(user_flow_info_id=int(user_flow_id)).all()
    return_datas = []
    for pro in pros:
        data = {}
        data['step_action'] = handling_suggestion[pro.step_action]
        data['desc'] = pro.desc
        data['step_time'] = pro.step_time
        return_datas.append(data)
    return ok(return_datas)

workflow = Blueprint('flow', __name__, url_prefix='/work_flow')

@workflow.route('/', methods=['GET', 'POST'])
def get_workfolws():
    if request.method=="GET":
        query = db.session.query(Workflow)
        workflows = query.all()
        convert = ObjectToDictEx([Role, WorkflowStep])
        objs = convert(workflows)
        if workflows:
            return ok(objs)


@workflow.route('/user', methods=['GET', 'POST'])
def user_workfolws():
    try:
        user = flask_login.current_user
        if request.method=="GET":
            return ok('获取')
        elif request.method=="POST":
            return ok('创建')
    except Exception as e:
        return err(e.args())