# coding:utf-8

from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

is_debug = True
app = Flask(__name__, template_folder='html/views',
            static_folder='html', static_url_path='/html')
CORS(app, supports_credentials=True)
admin = Admin(app, name="managesystem", template_mode="bootstrap3")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@127.0.0.1:3306/ftest'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 加入这些，admin可以增加数据
app.secret_key = 'workflowasdf'
app.config['SESSION_TYPE'] = 'filesystem'

# 登陆管理
# 声明login对象
login_manager = LoginManager()
# 初始化绑定到应用
login_manager.init_app(app)

# 声明默认视图函数为login，当我们进行@require_login时，如果没登陆会自动跳到该视图函数处理
login_manager.login_view = "login.login"

db = SQLAlchemy(app)
# 这里要导入蓝图
from managesys.service.login import login
from managesys.service.role import role
from managesys.service.work_flow import work_flow

# 在这里注册buleprint
app.register_blueprint(login.login_bp)
app.register_blueprint(work_flow.work_flow)
app.register_blueprint(role.role)
db.create_all()
