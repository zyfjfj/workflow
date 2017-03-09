# coding=utf-8 
"""
@version: ??
@author: zhayufeng
@describe:
@contact: zyfjfj@163.com
@software: PyCharm
@file: main.py
@time: 2016/12/29 17:23
"""
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.options
from managesys import app

if __name__=="__main__":
    tornado.options.parse_command_line()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()