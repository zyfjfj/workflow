#coding:utf8
import simplejson as json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.dynamic import AppenderQuery
import new
import datetime

def get_encoder(include_path=[],exclude_property=[]):
    class AlchemyEncoder(json.JSONEncoder):
        include=include_path
        exclude=exclude_property
        def default(self, obj,current_path=""):
            '''if isinstance(obj.__class__, DeclarativeMeta):
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    if field in self.exclude:
                        continue
                    value = obj.__getattribute__(field)
                    if isinstance(value,new.instancemethod):
                        continue
                    elif isinstance(value,AppenderQuery):
                        continue
                    elif isinstance(value,datetime.datetime):
                        value=str(value)
                    elif isinstance(value,list):
                        if len(current_path)==0:
                            if field not in self.include:
                                continue
                            for v in value:
                                result.append(self.default(v,field))
                            value=result
                        else:
                            if current_path+"."+field not in self.include:
                                continue
                            result=[]
                            for v in value:
                                result.append(self.default(v,current_path+"."+field))
                            value=result
                    elif isinstance(value.__class__, DeclarativeMeta):
                        if len(current_path)==0:
                            if field not in self.include:
                                continue
                            value=self.default(value,field)
                        else:
                            if current_path+"."+field not in self.include:
                                continue
                            value=self.default(value,current_path+"."+field)
                    try:
                        json.dumps(value)
                        fields[field] = value
                    except TypeError as e:
                        log.error("JSON序列化数据异常 原因：%s"%(e))
                    except Exception as e:
                        pass
                return fields'''
            if isinstance(obj,datetime.datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder

class JsonSerializer:
    @classmethod
    def ser_query_result(cls,obj,total,success=True,include_path=[],exclude=[]):
        result={"success":success,"data":obj,"total":total}
        return json.dumps(result,cls=get_encoder(include_path=include_path,exclude_property=exclude))
    @classmethod
    def ser_get_one_result(cls,obj,success=True,include_path=[],exclude=[]):
        result={"success":True,"data":obj}
        return json.dumps(result,cls=get_encoder(include_path=include_path,exclude_property=exclude))
    @classmethod
    def ser_create_result(cls,obj,success=True,include_path=[],exclude=[]):
        result={"success":success,"data":obj}
        return json.dumps(result,cls=get_encoder(include_path=include_path,exclude_property=exclude))
    @classmethod
    def ser_common_failed_result(cls,tag="",is_write_tag=True):
        if is_write_tag:
            result={"success":False,"tag":tag}
        else:
            result={"success":False}
        return json.dumps(result)
    @classmethod
    def ser_common_succeed_result(cls,tag="",is_write_tag=False):
        if is_write_tag:
            result={"success":True,"tag":tag}
        else:
            result={"success":True}
        return json.dumps(result)
    @classmethod
    def ser_delete_result(cls,r=True):
        result={"success":r}
        return json.dumps(result)
    @classmethod
    def ser_login_result(cls,r,tag=""):
        result={"success":r,"tag":tag}
        return json.dumps(result)
    @classmethod
    def ser_logout_result(cls,r=True,tag=""):
        result={"success":r,"tag":tag}
        return json.dumps(result)
    @classmethod
    def ser_session_check_result(cls,r):
        result={"success":r}
        return json.dumps(result)
    @classmethod
    def ser_user_defined(cls,d):
        return json.dumps(d,cls=get_encoder([]))
