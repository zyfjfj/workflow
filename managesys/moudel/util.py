# coding:utf-8

from flask import json

from managesys import db

def objs_to_json(objs):
    if isinstance(objs, list):
        json_obj=[]
        for obj in objs:
            if isinstance(obj, db.Model):
                fields={}
                for field in [x for x in dir(obj) if not x.startswith('_') and x!= 'metadata' and x!='query' and x!='query_class']:
                    data=obj.__getattribute__(field)
                    try:
                        json.dumps(data)
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
                json_obj.append(fields)
        return json_obj

def ok(datas):
    return json.dumps({"status":200,"datas":datas})