# flask做的工作流的服务

## 两种方式运行
1. 用torndao做web服务，调用flask代码（main.py）
```
if __name__=="__main__":
    tornado.options.parse_command_line()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
```
2. runserver.py,用flask自己做web服务（runserver.py）

```
app.run(debug=True)
```

## 组织结构
1. 主目录底下__init__.py配置了数据库，注册了blueprint；
2. moudel目录下放该工程用的的工具
3. service放服务，业务逻辑都在这里实现，在每个服务下，初始化Blueprint
```
work_flow = Blueprint('work_flow', __name__, url_pr+efix='/workflow')

```
## 中间件的使用
1. flask_admin中间件，在主目录下__init__.py加入代码，在定义数据库的地方，加入要管理的表
    ```
    admin=Admin(app,name="managesystem",template_mode="bootstrap3")
    ```
    ```
    class UserView(ModelView):
        # 是否允许创建
        can_create = False
        # 显示的字段
        column_searchable_list = ('username', 'email')

        def is_accessible(self):
            return is_debug

        def __init__(self, session, **kwargs):
            super(UserView, self).__init__(User, session, **kwargs)

    admin.add_view(UserView(db.session))
    ```
2. flask_login中间件        
    ```
    # 声明login对象
    login_manager = LoginManager()
    login_manager.init_app(app)
    # 声明默认视图函数为login，当我们进行@require_login时，如果没登陆会自动跳到该视图函数处理
    login_manager.login_view = "login"

    # 当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载用户对象。它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
    @login_manager.user_loader
    def load_user(userid):
        return User.query.get(int(userid))
    ```
3. sqlalchemy的用法
    1. 要让sqlalchemy创建数据库要在两个地方引用，以workflow为例
        1. 在workflow包中的wrok_flow.py引入
        ```
        import models

        ```
        2. 在工程__init__.py引入
        
        ```
        from managesys.service.workflow import work_flow
        ```
4. [一套完整自定义工作流的实现](http://www.cnblogs.com/walkingp/archive/2010/08/09/1795527.html)
## 注意事项
    1. blueprint中已经有role，自己的role命名成了app_role
    2. role\models.py中，要加入
    ```
    from ..work_flow.models import FlowInfo
    #为了这个能找到
    flow_info=db.relationship("FlowInfo")
    ```