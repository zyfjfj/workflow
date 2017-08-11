# coding:utf-8
import uuid

from flask import json
from managesys import db


class ObjectToDictEx(object):
    '''
    将sqlalchemy实例转成json
    '''
    def __init__(self, exclude_property=[]):
        self.exclude_property = exclude_property

    def _to_json(self, obj):
        if isinstance(obj, db.Model):
            fields = {}
            for field in [x for x in dir(obj) if
                          not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
                data = obj.__getattribute__(field)
                if isinstance(data, list):
                    exclude_propertys=[]
                    for d in data:
                        for property in self.exclude_property:
                            if isinstance(d, property):
                                exclude_propertys.append(_to_json(d))
                    fields[field] = exclude_propertys
                    continue
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
    def objs_to_json(self,objs):
        '''
        将数据库的实体转成json数据
        :param objs:
        :return:
        '''
        json_obj = []
        if isinstance(objs, list):
            for obj in objs:
                fields = self._to_json(obj)
                json_obj.append(fields)
        else:
            json_obj.append(self._to_json(objs))
        return json_obj
    def __call__(self, objs):
        return self.objs_to_json(objs)

def _to_json(obj):
    if isinstance(obj, db.Model):
        fields = {}
        for field in [x for x in dir(obj) if
                      not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
            data = obj.__getattribute__(field)
            if isinstance(data, list):
                for d in data:
                    fields[field] = d.name
                continue
            try:
                json.dumps(data)
                fields[field] = data
            except TypeError:
                fields[field] = None
        return fields
def objs_to_json(objs):
    '''
    将数据库的实体转成json数据
    :param objs:
    :return:
    '''
    json_obj = []
    if isinstance(objs, list):
        for obj in objs:
            fields = _to_json(obj)
            json_obj.append(fields)
    else:
        json_obj.append(_to_json(objs))
    return json_obj
def ok(datas):
    return json.dumps({"status": 200, "data": datas})


def err(datas, status=401):
    return json.dumps({"status": status, "data": datas})


def generate_uuid():
    return uuid.uuid4().hex
