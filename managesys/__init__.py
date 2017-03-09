#coding:utf-8

from flask import Flask
from flask_admin import Admin

from flask_sqlalchemy import SQLAlchemy

is_debug=True
app = Flask(__name__)
admin=Admin(app,name="managesystem",template_mode="bootstrap3")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@127.0.0.1:3306/ftest'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True
db = SQLAlchemy(app)
#这里要导入蓝图
from managesys.service.login import login
from managesys.service.workflow import work_flow
from managesys.service.screen import models
#在这里注册buleprint
app.register_blueprint(login.login)
app.register_blueprint(work_flow.work_flow)
db.create_all()