# -*- coding:utf-8 -*-  
"""
@version: ??
@author: zhayufeng
@describe:
@contact: zyfjfj@163.com
@software: PyCharm
@file: asyn
@time: 2017/8/15 15:37
"""
# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer

from managesys import app

monkey.patch_all()
# gevent end

if __name__ == "__main__":
    # app.run()
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()