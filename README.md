# flask的一个练习

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
4. 用了admin中间件，在主目录下__init__.py加入代码，在定义数据库的地方，加入要管理的表
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

