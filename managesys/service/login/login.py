# coding:utf-8
from flask import Blueprint,request
from flask import flash,json

from flask_login import login_user,logout_user

from managesys import login_manager
from managesys.moudel.util import objs_to_json,ok
from models import User

login_bp = Blueprint('login', __name__, url_prefix='/login')

# 当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载用户对象。它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@login_bp.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        user=json.loads(request.data)
        user=User.query.filter_by(id=user["id"]).first()
        if user:
            login_user(user)
            return json.dumps(objs_to_json(user))
        else:
            return "error"
    else:
        users=User.query.all()
        if users:
            login_user(users[0])
            return ok(objs_to_json(users))
        return 'Hello World!'
