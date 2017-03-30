# coding:utf-8
from flask import Blueprint,request,render_template,redirect,url_for,session
from flask import flash,json

from flask_login import login_user,logout_user,login_required

from managesys import login_manager,app
from managesys.moudel.util import objs_to_json,ok, err
from models import User

login_bp = Blueprint('login', __name__, url_prefix='/login')

# 当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载用户对象。它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))
    
@app.route('/index')
@login_required
def index():
    user=User.query.filter_by(id=session['user_id'])
    if user:
        user=user.first()
        workflows = [{"name": u"选择流程", "id": 0}]
        for role in user.roles:
            for flow in role.flow_infos:
                workflows.append({"name": flow.name, "id": flow.id})
        return render_template('index.html',workflows=workflows,username=user.name)
@login_bp.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        #user=json.loads(request.data)
        email=request.form['email']
        password=request.form['password']        
        user=User.query.filter_by(email=email,password=password).first()
        if user:
            login_user(user)
            #return json.dumps(objs_to_json(user))
            #return render_template('index.html',workflows=workflows,username=user.name) 这种方式链接不会改
            return redirect(url_for('index'))
        else:
            return err("用户密码错误")
    elif request.method=="GET":        
        return render_template('login.html')
