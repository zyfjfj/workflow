# coding:utf-8
from flask import Blueprint,request

from managesys.moudel.util import objs_to_json,ok
from models import User

login = Blueprint('login', __name__, url_prefix='/login')

@login.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        pass
    else:
        users=User.query.all()
        if users:
            return ok(objs_to_json(users))
        return 'Hello World!'