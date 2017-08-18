# coding:utf-8
from operator import attrgetter

import flask_login
import time
from flask import Blueprint, json
from flask import request, session, redirect, url_for, render_template
from flask_login import login_required
from ... import db, app
from ...model.models import User, FlowInfo, TranctProc, UserFlowInfo, Role
from ...moudel.util import ok, objs_to_json, ObjectToDictEx, err
from ...model.work_flow_models import Workflow, WorkflowStep, UserWorkflowInfo, UserWorkflowInfoDetail, WorkflowComment

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
        else:
            return ok('没有数据')


@workflow.route('/user', methods=['GET', 'POST','PUT'])
def user_workfolws():
    try:
        user = flask_login.current_user
        if request.method=="GET":
            user_id = request.args.get('user_id', '')
            u_workflow_infos = UserWorkflowInfo.query.filter_by(user_id=user_id).all()
            convert = ObjectToDictEx([Role, WorkflowStep])
            objs = convert(u_workflow_infos)
            return ok(objs)
        elif request.method=="POST":
            workflow_id = request.form['workflow_id']
            user_id = request.form['user_id']
            comment=request.form['comment']
            desc=request.form['desc']
            user = User.query.get(user_id)
            workflow=Workflow.query.get(workflow_id)
            workflow_step=None
            role=None
            for r in user.roles:
                workflow_step=WorkflowStep.query.filter_by(workflow_id=workflow_id,role_id=r.id).first()
                if workflow_step:
                    role=r
                    break
            if workflow_step is None:
                return err("该用户没有权限")
            user_workflow_info=UserWorkflowInfo(role=role,workflow_id=workflow_id,step_id=workflow_step.id,
                                                 next_role=workflow_step.next_step[0].role,user_id=user_id)
            db.session.add(user_workflow_info)
            db.session.flush()
            u_workflow_detail=UserWorkflowInfoDetail(comment=comment,user_workflow_info_id=user_workflow_info.id
                                                     ,desc=desc)
            db.session.add(u_workflow_detail)
            db.session.commit()
            return ok('创建')
        elif request.method=="PUT":
            data = json.loads(request.data)
            u_workflow_info_id=data['u_workflow_info_id']
            user_id=data['user_id']
            desc=data['desc']
            comment=data['comment']
            u_workflow_info = UserWorkflowInfo.query.get(u_workflow_info_id)
            user = User.query.get(user_id)
            role=None
            workflow_step=None
            for r in user.roles:
                workflow_step = WorkflowStep.query.filter_by(workflow_id=u_workflow_info.workflow_id, role_id=r.id).first()
                if workflow_step:
                    role = r
                    break
            if workflow_step is None:
                return err("没有找到")
            if comment == WorkflowComment.Agree:#同意
                u_workflow_info.role=role
                u_workflow_info.step_id = workflow_step.id
                if workflow_step.next_step:
                    u_workflow_info.next_role = workflow_step.next_step[0].role
                else:
                    u_workflow_info.is_finish = True
            elif comment==WorkflowComment.Refuse:
                u_workflow_info.is_finish=True
            elif comment==WorkflowComment.Abort:
                u_workflow_info.is_finish = True
            u_workflow_detail = UserWorkflowInfoDetail(comment=comment, user_workflow_info_id=u_workflow_info.id,
                                                       desc=desc)
            db.session.add(u_workflow_detail)
            db.session.commit()
            return ok('you')
    except Exception as e:
        return err(e.args())

@workflow.route('/bokeh')
def bokeh():
    from bokeh.plotting import figure, output_file,show
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    # output to static HTML file
    output_file("../../blines.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)
    show(p)
    return render_template('workflow.html')

@app.route('/asyn/', methods=['GET'])
def test_asyn_one():
    print("asyn has a request!")
    time.sleep(10)
    return 'hello asyn'

@app.route('/test/', methods=['GET'])
def test():
    def ssss():
        print("ssss")
        return "11111"
    f=lambda x,y,z:x+y+z
    print(f(1,2,3))
    ff=lambda :ssss()
    print(ff())
    return 'hello test'
