# coding:utf-8

from flask import json
from managesys import db
def _to_json(obj):
    if isinstance(obj, db.Model):
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
            data = obj.__getattribute__(field)
            if isinstance(data, list):
                for d in data:
                    fields[field]= d.name
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
    json_obj=[]
    if isinstance(objs,list):
        for obj in objs:
            fields=_to_json(obj)
            json_obj.append(fields)
    else:
        json_obj.append(_to_json(objs))
    return json_obj

def ok(datas):
    return json.dumps({"status":200,"data":datas})

def err(datas,status=401):
    return json.dumps({"status":status,"data":datas})