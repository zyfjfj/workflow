# coding=utf-8 
"""
@version: ??
@author: zhayufeng
@describe:
@contact: zyfjfj@163.com
@software: PyCharm
@file: role.py
@time: 2017/3/25 11:15
"""
from flask import Blueprint,request

from managesys.moudel.util import ok,objs_to_json
from models import Role

role = Blueprint('app_role', __name__, url_prefix='/role')

@role.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        pass
    else:
        roles=Role.query.all()
        if roles:
            return ok(objs_to_json(roles))
        return ok(u"没有数据")

