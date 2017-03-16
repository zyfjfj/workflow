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
work_flow = Blueprint('work_flow', __name__, url_prefix='/workflow')

```
